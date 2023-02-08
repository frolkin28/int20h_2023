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
import LoginPage from "../Pages/LoginPage";
import RegisterPage from "../Pages/RegisterPage";
import ContextWrapper from "./ContextWrapper";
import AuthRoute from "../AuthRoute";

import "./App.css";
import "../../universal-styles/RecipePreview.css";

function App() {
  return (
    <Router>
      <ContextWrapper>
        <div className="App">
          <Nav />
          <Switch>
            <Route path="/login" component={LoginPage} />
            <Route path="/Register" component={RegisterPage} />
            <Route path="/" exact component={Home} />
            <Route path="/ingredients" exact component={Ingredients} />
            <AuthRoute path="/user" exact component={User} />
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
      </ContextWrapper>
    </Router>
  );
}

export default App;
