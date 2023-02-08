import './style/Home.css';
import React from 'react';
import FeaturedRecipesList from '../FeaturedRecipes/FeaturedRecipesList';

function Home()
{
    return(
        <div className='home-page'>
            <FeaturedRecipesList />
        </div>
    )
}

export default Home;
