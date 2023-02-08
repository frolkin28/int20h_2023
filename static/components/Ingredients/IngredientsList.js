import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';

import LoadingPage from '../Pages/LoadingPage';
import { useUser } from '../../context/UserContext';

import './style/IngredientsList.css';


function IngredientsList(props) {
    const [ingredients, setIngredients] = useState([]);
    const [loading, setLoading] = useState(true);

    // setTimeout(() => setLoading(false), 5000);
    const [categoryTypes, setCategoryTypes] = useState([]);
    const [ingredientType, setIngredientType] = useState(null);

    const [page, setPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);
    const [showUser, setShowUser] = useState(false);
    const moreIngredientsHandler = () => setPage(page + 1);
    const { user } = useUser();

    const selectIngredients = e => {
        setIngredientType(e.target.value);
        setPage(1);
    }

    const handleChangeShowUser = () => setShowUser(!showUser);

    const addIngredient = (ingredientId) => {
        fetch('/api/user/product', {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            body: JSON.stringify({ product_id: ingredientId })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'success') return;
                console.log('Successful added');
            })
    };

    useEffect(() => {
        setPage(1);
    }, props.searchWord)

    useEffect(() => {
        fetch(`/api/ingredient/search`, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            body: JSON.stringify({
                page,
                ingredient_type: ingredientType,
                query: props.searchWord,
                for_user: !!user && showUser
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'success') return;
                setLoading(false);
                if (ingredientType && page === 1 || props.searchWord && page === 1) setIngredients(data.payload.ingredients);
                else setIngredients([...ingredients, ...data.payload.ingredients]);
                setNextPage(data.payload.nextPage);
            });
    }, [page, ingredientType, props.searchWord, user, showUser]);

    useEffect(() => {
        fetch(`/api/ingredient_types`, {
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
        })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'success') return;
                setCategoryTypes(data.payload);
            });
    }, []);

    return (
        <>
            {loading === true ? (
                <LoadingPage />
            ) : (
                <div className='home-page ingredients' id='ingredients'>
                    <div className='ingredients-declaration'>Search by Ingredient</div>
                    <select name="select-ingredients" onChange={selectIngredients}>
                        <option value="">--Please choose the category--</option>
                        {categoryTypes.map((categoryType) => (
                            <option className="dropdown__option" key={categoryType.title}>{categoryType.title}</option>
                        ))}
                    </select>
                    {user &&
                        <label>
                            <input type="checkbox" checked={showUser} onChange={handleChangeShowUser} />
                            Show only recipes available for user
                        </label>
                    }
                    <div className='ingredient-list'>
                        {ingredients.map((ingredient) => (
                            <div className='ingredient' key={ingredient._id}>
                                <Link to={{
                                    pathname: `/ingredients/${ingredient.title}`, state: { ingredient }
                                }}>
                                    <img className='ingredient-thumbnail' src={`https://www.themealdb.com/images/ingredients/${ingredient.title}.png`} alt='T_T' />
                                    <div className='ingredient-name'>{ingredient.title}</div>
                                </Link>
                                <div className='button-container'>
                                    <button className='recipe-but' onClick={() => addIngredient(ingredient._id)}>Add</button>
                                </div>
                            </div>
                        ))}
                    </div>
                    {nextPage !== null ? (
                        <div className='button-container '>
                            <button className='recipe-but more' onClick={moreIngredientsHandler}>More Ingredients</button>
                        </div>
                    ) : (
                        <></>
                    )}
                </div>
            )}
        </>
    );
}

export default IngredientsList;
