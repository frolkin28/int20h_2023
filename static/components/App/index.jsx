import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Nav from "../Nav/Nav";
import Home from "../Pages/Home";
import SearchRecipes from "../Recipes/SearchRecipes";
import RecipeDetails from "../Recipes/RecipeDetails";
import CategoryDetails from "../Categories/CategoryDetails";
import IngredientDetails from "../Ingredients/IngredientDetails";
import AreaRecipes from "../Areas/AreaRecipes";
import Page404 from "../Pages/Page404";
import Ingredients from "../Pages/Ingredients";
import User from "../Pages/User";
import Footer from "../Footer/Footer";

import "./App.css";
import "../../universal-styles/RecipePreview.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Nav />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/ingredients" exact component={Ingredients} />
          <Route path="/user" exact component={User} />
          <Route path="/recipes/id/:id" exact component={RecipeDetails} />
          <Route
            path="/recipes/search/:pathname/:input"
            exact
            component={SearchRecipes}
          />
          <Route path="/categories/:name" exact component={CategoryDetails} />
          <Route
            path="/ingredients/:ingredient"
            exact
            component={IngredientDetails}
          />
          <Route path="/area/:area" exact component={AreaRecipes} />
          <Route component={Page404} />
        </Switch>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
