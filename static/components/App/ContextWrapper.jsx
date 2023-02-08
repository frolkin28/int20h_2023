import React from "react";

import { UserContextProvider } from "../../context/UserContext";

const ContextWrapper = ({ children }) => {
  return <UserContextProvider>{children}</UserContextProvider>;
};

export default ContextWrapper;
