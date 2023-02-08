import './style/IngredientsList.css';
import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import LoadingPage from '../Pages/LoadingPage';
import Page404 from '../Pages/Page404';

function IngredientsList(props)
{
    const [ingredients, setIngredients] = useState([]);
    const [loading, setLoading] = useState(true);

    setTimeout(() => setLoading(false), 5000);
    const [categoryTypes, setCategoryTypes] = useState([]);
    const [ingredientType, setIngredientType] = useState(null);

    const [page, setPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);
    const moreIngredientsHandler = () => setPage(page + 1);
    const addIngredient = () => 1;

    const selectIngredients = e => {
        setIngredientType(e.target.value);
        setPage(1);
    }

    useEffect(() => {
        setPage(1);
    }, props.searchWord)

    useEffect(() => {
        fetch(`/api/ingredient/search`,{
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            body: JSON.stringify(
                {page, ingredient_type: ingredientType, query: props.searchWord}
            )
        })
            .then(response => response.json())
            .then(data => {
                if(data.status !== 'success') return;
                setLoading(false);
                if (ingredientType && page === 1 || props.searchWord && page === 1) setIngredients(data.payload.ingredients);
                else setIngredients([...ingredients, ...data.payload.ingredients]);
                setNextPage(data.payload.nextPage);
            });
    }, [page, ingredientType, props.searchWord]);

    useEffect(() => {
        fetch(`/api/ingredient_types`,{
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
        })
            .then(response => response.json())
            .then(data => {
                if(data.status !== 'success') return;
                setCategoryTypes(data.payload);
            });
    }, []);

    return(
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
                <div className='ingredient-list'>
                    {ingredients.map((ingredient) => (
                        <div className='ingredient' key={ingredient._id}>
                            <Link to={{
                                pathname:`/ingredients/${ingredient.title}`, state: { ingredient }
                            }}>
                                <img className='ingredient-thumbnail' src={`https://www.themealdb.com/images/ingredients/${ingredient.title}.png`} alt='T_T'/>
                                <div className='ingredient-name'>{ingredient.title}</div>
                            </Link>
                            <div className='button-container'>
                                <button className='recipe-but' onClick={addIngredient}>Add</button>
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
