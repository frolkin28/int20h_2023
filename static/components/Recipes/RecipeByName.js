import React, { useEffect, useState } from 'react';
import {Link} from 'react-router-dom';
import LoadingPage from '../Pages/LoadingPage';
import Page404 from '../Pages/Page404';

import '../../universal-styles/RecipePreview.css';

function RecipePreview({recipe})
{

    return(
        <>
            <div className='recipe'>
                <Link to={`/recipes/id/${recipe._id}`} className='recipe-link'>
                    <div className='recipe-name'>{recipe.title}</div>
                    <img className='recipe-image' src={recipe.img_url} alt='T_T'/>
                    <button className='recipe-but'>Переглянути</button>
                </Link>
            </div>
        </>
    );
}

export default RecipePreview;
