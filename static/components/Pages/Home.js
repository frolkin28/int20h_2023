import './style/Home.css';
import React from 'react';
import FeaturedRecipesList from '../FeaturedRecipes/FeaturedRecipesList';
import Footer from "../Footer/Footer";

function Home()
{
    return(
        <div className='home-page'>
            <FeaturedRecipesList />
        </div>
    )
}

export default Home;
