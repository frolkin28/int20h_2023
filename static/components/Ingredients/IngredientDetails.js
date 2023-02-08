import './style/IngredientDetails.css';
import React from 'react';
import IngredientRecipes from './IngredientRecipes';

function IngredientDetails({location})
{
    const {ingredient} = location.state;

    return (
        <>
            <div className='ingredient-page'>
                <div className='ingredient-name'>{ingredient.title}</div>
                <img className='ingredient-image' src={`https://www.themealdb.com/images/ingredients/${ingredient.title}.png`} alt='T_T' />
                <p className='ingredient-description'>{ingredient.description}</p>
                <IngredientRecipes id={ingredient._id} title={ingredient.title} />
            </div>
        </>
    );
}

export default IngredientDetails;