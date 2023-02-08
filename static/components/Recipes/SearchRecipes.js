import React from 'react';
import IngredientsList from "../Ingredients/IngredientsList";
import FeaturedRecipesList from "../FeaturedRecipes/FeaturedRecipesList";

function SearchRecipes({ match }) {
    const searchBy = match.params.pathname;
    const input = match.params.input;

    return (
        <>
            {searchBy === 'ingredients' ? (
                <IngredientsList searchWord={input} />
            ) : searchBy === 'recipes' ? (
                <FeaturedRecipesList searchWord={input} />
            ) : (
                <></>
            )}
        </>
    );
}

export default SearchRecipes;
