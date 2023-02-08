import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import LoadingPage from '../Pages/LoadingPage';
import Page404 from '../Pages/Page404';

function UserDetails(props)
{
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    setTimeout(() => setLoading(false), 5000);

    const [ingredients, setIngredients] = useState([]);
    const [ingredientsNum, setIngredientsNum] = useState(10);

    const moreIngredientsHandler = () => setIngredientsNum(ingredientsNum + 10);

    useEffect(() => {
        //fetch(`/api/ingredients/`)
        fetch(`https://www.themealdb.com/api/json/v1/1/list.php?i=list`)
            .then(response => response.json())
            .then(data => {
                if(data.meals === null) return;
                setLoading(false);
                setIngredients(data.meals);
            });
    }, []);

    return(
        <>
            {/*{loading === true ? (*/}
            {/*    <LoadingPage />*/}
            {/*) : loading === false && user === null && ingredients.length === 0 ? (*/}
            {/*    <Page404 />*/}
            {/*) : (*/}
            <div className='home-page ingredients' id='ingredients'>
                <div className='ingredients-declaration'>HELLO, user.name</div>
                <div className='ingredient-list'>
                    {ingredients.slice(0, ingredientsNum).map((ingredient, index) => (
                        <div className='ingredient' key={index}>
                            <Link to={`/ingredients/${ingredient.strIngredient}`}>
                                <img className='ingredient-thumbnail' src={`https://www.themealdb.com/images/ingredients/${ingredient.strIngredient}.png`} alt='T_T'/>
                                <div className='ingredient-name'>{ingredient.strIngredient}</div>
                            </Link>
                            <div className='button-container'>
                                <button className='button'>Delete</button>
                            </div>
                        </div>
                    ))}
                </div>
                {ingredients.length > ingredientsNum ? (
                    <div className='button-container'>
                        <button className='recipe-but more' onClick={moreIngredientsHandler}>More Ingredients</button>
                    </div>
                ) : (
                    <></>
                )}
            </div>
            {/*)}*/}
        </>
    );
}

export default UserDetails;
