import logging
import typing as t

from bson import ObjectId
from decimal import Decimal
from paginate import Page

from hackaton.const import (
    PAGE_NUMBER_PARAM,
    SORT_PARAM,
    INGREDIENTS_IDS_PARAM,
    CREATED_BY_USER_IDS_PARAM,
    AREA_PARAM,
    SourceTypeEnum,
    INGREDIENT_TYPE_PARAM,
    RECIPE_CATEGORY_PARAM,
    PAGE_SIZE_PARAM,
    QUERY_STRING_PARAM,
)

log = logging.getLogger(__name__)


class BaseSearchMongoExecutor:
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    DOCS_LIMIT = 10000

    def __init__(
        self, db: t.Any, filter_data: t.Dict, debug: bool = False
    ) -> None:
        self.db = db
        self.filter_data = filter_data
        self.debug = debug
        self._data = None

    async def get_result(self) -> t.Optional[t.List[t.Dict[str, t.Any]]]:
        if self._data is None:
            query, sort_query = self._build_query()

            skip, limit = self.slice
            cursor = self.db.find(query).skip(skip).limit(limit)

            if sort_query:
                cursor.sort(sort_query)

            self._data = await cursor.to_list(length=self.page_size)

        return self._data

    @property
    def page(self) -> int:
        page = self.filter_data.get(PAGE_NUMBER_PARAM, 1)
        return max(page, 1)

    @property
    def page_size(self) -> int:
        page_size = (
            self.filter_data.get(PAGE_SIZE_PARAM, self.DEFAULT_PAGE_SIZE)
        )
        return min(page_size, self.MAX_PAGE_SIZE)

    @property
    def slice(self) -> tuple:
        start = (self.page - 1) * self.page_size
        end = self.page * self.page_size
        return start, end

    async def get_pager(self) -> Page:
        return Page(
            await self.get_result(),
            page=self.page,
            items_per_page=self.page_size,
            item_count=await self._get_count(),
        )

    async def _get_count(self) -> int:
        query, _ = self._build_query()
        count = await self.db.count_documents(query)
        return min(count, self.DOCS_LIMIT)

    @staticmethod
    def _exists(
        field_name: str, cond: bool = True
    ) -> t.Optional[t.Dict[str, t.Any]]:
        if not field_name or cond is None:
            return None
        return {field_name: {'$exists': cond}}

    @staticmethod
    def _in(
        field_name: str, choices: t.Optional[t.List[str]]
    ) -> t.Optional[t.Dict[str, t.Any]]:
        if not field_name or not choices:
            return None

        return {field_name: {'$in': choices}}

    @staticmethod
    def _and(
        conditions: t.List[t.Optional[t.Dict[str, t.Any]]]
    ) -> t.Optional[t.Dict[str, t.List[t.Optional[t.Dict[str, t.Any]]]]]:
        if not conditions:
            return None
        return {'$and': conditions}

    @staticmethod
    def _or(
        conditions: t.Optional[t.List[t.Dict[str, t.Any]]]
    ) -> t.Optional[t.Dict[str, t.List[t.Dict[str, t.Any]]]]:
        if not conditions:
            return None
        return {'$or': conditions}

    @staticmethod
    def _range(
        field_name: str,
        value_from: t.Optional[str],
        value_to: t.Optional[str]
    ) -> t.Optional[t.Dict[str, t.Dict[str, t.Any]]]:
        if not field_name or not any([bool(value_from), bool(value_to)]):
            return None
        if isinstance(value_from, Decimal):
            value_from = float(value_from)
        if isinstance(value_to, Decimal):
            value_to = float(value_to)

        query = {}
        if value_from:
            query['$gte'] = value_from
        if value_to:
            query['$lte'] = value_to

        return {field_name: query}

    @staticmethod
    def _sort(
        sort_keys: t.Optional[t.List[str]]
    ) -> t.Optional[t.List[t.Tuple[str, int]]]:
        if not sort_keys:
            return None

        query = []
        for key in sort_keys:
            if key.startswith('-'):
                _key = key[1:]
                query.append((_key, -1))
            else:
                query.append((key, 1))

        return query

    def _build_query(self) -> (
        t.Tuple[
            t.Optional[t.Dict[str, t.Any]],
            t.Optional[t.List[t.Tuple[str, int]]]
        ]
    ):
        raise NotImplementedError()

    @staticmethod
    def created_by_user_ids_filter(user_ids: t.List[str]):
        if not user_ids:
            return None

        return {
            'source.type': SourceTypeEnum.user.value,
            'source.id': {'$in': user_ids}
        }

    @staticmethod
    def _query_string_filter(query_string: str):
        if not query_string:
            return None

        return {
            '$text': { '$search': query_string }
        }


class RecipeSearchMongoExecutor(BaseSearchMongoExecutor):
    def _build_query(self) -> (
        t.Tuple[
            t.Optional[t.Dict[str, t.Any]],
            t.Optional[t.List[t.Tuple[str, int]]]
        ]
    ):
        query_string_filter = self._query_string_filter(
            self.filter_data.get(QUERY_STRING_PARAM)
        )

        ingredients_ids_filter = self._ingredients_ids_filter(
            ingredients_ids=self.filter_data.get(INGREDIENTS_IDS_PARAM)
        )

        created_by_user_ids_filter = self.created_by_user_ids_filter(
            user_ids=self.filter_data.get(CREATED_BY_USER_IDS_PARAM)
        )

        area_filter = self._in(
            field_name='area',
            choices=self.filter_data.get(AREA_PARAM)
        )

        recipe_category_filter = self._in(
            field_name='category',
            choices=self.filter_data.get(RECIPE_CATEGORY_PARAM)
        )

        filters = [
            query_string_filter,
            ingredients_ids_filter,
            created_by_user_ids_filter,
            area_filter,
            recipe_category_filter,
        ]

        filters = [f for f in filters if f]

        if not filters:
            query = {}
        elif len(filters) == 1:
            query = filters[0]
        else:
            query = self._and(conditions=filters)

        sort_keys = self.filter_data.get(SORT_PARAM)
        sort_query = self._sort(sort_keys)

        if self.debug:
            log.info(
                f'\n\n\n\n{"#" * 100}\n '
                f'query {query} \n\n sort_query {sort_query} '
                f'\n{"#" * 100}\n\n'
            )

        return query, sort_query

    @staticmethod
    def _ingredients_ids_filter(ingredients_ids: t.List[str]):
        if not ingredients_ids:
            return None

        if len(ingredients_ids) > 3:
            query = {
                'ingredients_ids': { '$in': ingredients_ids },
                '$expr': {
                    '$gte': [
                        { '$size': {
                            '$setIntersection':
                                ['$ingredients_ids', ingredients_ids]
                            }
                        },
                        3
                    ]
                }
            }
        else:
            query = {
                'ingredients.ingredient_id': {'$all': ingredients_ids}
            }

        return query


class IngredientSearchMongoExecutor(BaseSearchMongoExecutor):
    def _build_query(self) -> (
        t.Tuple[
            t.Optional[t.Dict[str, t.Any]],
            t.Optional[t.List[t.Tuple[str, int]]]
        ]
    ):
        query_string_filter = self._query_string_filter(
            self.filter_data.get(QUERY_STRING_PARAM)
        )

        created_by_user_ids_filter = self.created_by_user_ids_filter(
            user_ids=self.filter_data.get(CREATED_BY_USER_IDS_PARAM)
        )

        ingredient_type_filter = self._in(
            field_name='type',
            choices=self.filter_data.get(INGREDIENT_TYPE_PARAM)
        )

        ingredients_ids_filter = self._ingredients_ids_filter(
            ingredients_ids=self.filter_data.get(INGREDIENTS_IDS_PARAM)
        )

        filters = [
            query_string_filter,
            ingredients_ids_filter,
            created_by_user_ids_filter,
            ingredient_type_filter,
        ]

        filters = [f for f in filters if f]

        if not filters:
            query = {}
        elif len(filters) == 1:
            query = filters[0]
        else:
            query = self._and(conditions=filters)

        sort_keys = self.filter_data.get(SORT_PARAM)
        sort_query = self._sort(sort_keys)

        if self.debug:
            log.info(
                f'\n\n\n\n{"#" * 100}\n '
                f'query {query} \n\n sort_query {sort_query} '
                f'\n{"#" * 100}\n\n'
            )
        return query, sort_query

    def _ingredients_ids_filter(self, ingredients_ids: t.List[str]):
        if not ingredients_ids:
            return None

        return self._in(
            field_name='_id',
            choices=[ObjectId(_id) for _id in ingredients_ids]
        )
