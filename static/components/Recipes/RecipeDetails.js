import './style/RecipeDetails.css';
import React, {useEffect, useState} from 'react';
import Ingredient from './VisibleIngredient';
import LoadingPage from '../Pages/LoadingPage';
import Page404 from '../Pages/Page404';

function Recipe({match})
{
  const [recipe, setRecipe] = useState([]);
  const [loading, setLoading] = useState(true);
  setTimeout(() => setLoading(false), 5000);

  useEffect(() => {
    fetch(`http://0.0.0.0:8080/api/recipe/${match.params.id}`)
      .then(response => response.json())
      .then(data => {
        if(data.status !== 'success') return;
        setLoading(false);
        setRecipe(data.payload);
      })
    }, [match]);

  return (
    <>
    {loading === true ? (
      <LoadingPage />
    ) : loading === false && recipe.length === 0 ? (
      <Page404 />
    ) : (
      <div className='Recipe'>
        <div className='home-page block-content'>
          <div className='image-block'>
              <div className='name'>{recipe.title}</div>
            <img className='image' src={recipe.img_url} alt='T_T'></img>
            <div className='info'>
              <div className='tags'>Tags: {recipe.tags}</div>
              <div className='category'>Category: {recipe.category}</div>
              <div className='area'>Area: {recipe.area}</div>
              <div className='youtube-link' ><a href={recipe.video_url}>Video</a></div>
            </div>
          </div>
          <div className='ingredient-block'>
            <div className='ingredients-declaration'>Ingredients</div>
            <ul className='ingredients'>
                {recipe.ingredients.map((ingredient) => (
                    <Ingredient key={ingredient.ingredient_id} ingredient={ingredient.ingredient_title} measure={ingredient.measure} />
                ))}
            </ul>
          </div>
        </div>
        <div className='instructions-block'>
          <div className='instructions-declation'>Instructions</div>
          <div className='instructions'>{recipe.instructions}</div>
        </div>
      </div>
    )}
    </>
  );
}

export default Recipe;
