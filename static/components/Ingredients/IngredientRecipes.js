import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import LoadingPage from '../Pages/LoadingPage';
import Page404 from '../Pages/Page404';
import Recipe from "../Recipes/RecipeByName";

function IngredientRecipes(props)
{
    const ingredient_id = props.id;
    const ingredient_title = props.title;
    const [recipes, setRecipes] = useState([]);

    const [page, setPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);
    
    const [loading, setLoading] = useState(true);
    setTimeout(() => setLoading(false), 5000);

    const moreRecipesHandler = () => setPage(page + 1);

    useEffect(() => {
        fetch(`/api/recipe/search`, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            body: JSON.stringify({page, ingredients_ids: [ingredient_id]})
        })
            .then(response => response.json())
            .then(data => {
                if(data.status !== 'success') return;
                setRecipes([...recipes, ...data.payload.recipes])
                setNextPage(data.payload.nextPage);
                setLoading(false);
            });
    }, [page]);

    return(
        <>
        {loading === true ? (
            <LoadingPage />
        ) : loading === false && recipes.length === 0 ? (
            <Page404 />
        ) : (
            <div className='ingredients-recipes'>
                <div className='recipes-declaration'>Recipes containing {ingredient_title}.</div>
                <div className='recipes-list'>
                    {recipes.map((recipe) => (
                        <Recipe recipe={recipe} key={recipe._id}/>
                    ))}
                </div>
                {nextPage !== null ? (
                    <div className='button-container '>
                        <button className='recipe-but more' onClick={moreRecipesHandler}>More Recipes</button>
                    </div>
                ) : (
                    <></>
                )}
            </div>
        )}
        </>
    );
}

export default IngredientRecipes;