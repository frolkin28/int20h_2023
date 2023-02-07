import './style/Home.css';
import React from 'react';
import IngredientsList from '../Ingredients/IngredientsList';

function Ingredients()
{
    return(
        <div className='home-page'>
            <IngredientsList />
        </div>
    )
}

export default Ingredients;