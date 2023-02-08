import React from "react";
import { Redirect, Route } from "react-router-dom";

import { useUser } from "../../context/UserContext";

const AuthRoute = (props) => {
  const { user } = useUser();
  console.log("user", user);
  if (!user) {
    return <Redirect to="/login" />;
  }

  return <Route {...props} />;
};

export default AuthRoute;
