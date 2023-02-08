import React, { useEffect, useState } from 'react';
import Recipe from '../Recipes/RecipeByName';
import LoadingPage from "../Pages/LoadingPage";
import Page404 from "../Pages/Page404";
import { useUser } from '../../context/UserContext';

function FeaturedRecipesList(props) {
    const [recipes, setRecipes] = useState([]);
    const [page, setPage] = useState(1);
    const [nextPage, setNextPage] = useState(null);
    const [difficultyLevel, setDifficultyLevel] = useState(null);
    const [showUser, setShowUser] = useState(false);
    const difficultyLevels = ['-difficulty_level', '+difficulty_level']

    const [loading, setLoading] = useState(true);
    const { user } = useUser();

    const moreRecipesHandler = () => setPage(page + 1);
    const handleChangeShowUser = () => setShowUser(!showUser);

    const selectLevel = (e) => {
        setDifficultyLevel(e.target.value);
        setPage(1);
    }

    useEffect(() => {
        fetch(`/api/recipe/search`, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            body: JSON.stringify({
                page,
                query: props.searchWord,
                sort: difficultyLevel,
                for_user: !!user && showUser
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'success') return;
                setLoading(false);
                if (difficultyLevel && page === 1 || props.searchWord && page === 1) setRecipes(data.payload.recipes);
                else setRecipes([...recipes, ...data.payload.recipes])
                setNextPage(data.payload.nextPage);
            })
    }, [page, props.searchWord, difficultyLevel, user, showUser]);

    return (
        <>
            {loading === true ? (
                <LoadingPage />
            ) : loading === false && recipes.length === 0 ? (
                <Page404 />
            ) : (
                <div className='home-page recipes'>
                    <div className='recipes-declaration'>Top Recipes</div>
                    <select name="select-ingredients" onChange={selectLevel}>
                        <option value="">--Please choose the difficulty level--</option>
                        {difficultyLevels.map((level) => (
                            <option className="dropdown__option" key={level}>{level}</option>
                        ))}
                    </select>
                    {user && (
                        <label>
                            <input type="checkbox" checked={showUser} onChange={handleChangeShowUser} />
                            Show only user product
                        </label>
                    )
                    }
                    <div className='recipes-list'>
                        {recipes.map((recipe) => (
                            <Recipe recipe={recipe} key={recipe._id} />
                        ))}
                    </div>
                </div>
            )
            }
            {nextPage !== null ? (
                <div className='button-container '>
                    <button className='recipe-but more' onClick={moreRecipesHandler}>More Recipes</button>
                </div>
            ) : (
                <></>
            )}
        </>
    );
}

export default FeaturedRecipesList;
