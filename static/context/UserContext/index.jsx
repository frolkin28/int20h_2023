import React, { useEffect, useState } from "react";
import { useQuery } from "react-query";

const UserContext = React.createContext({});

export const useUser = () => {
  return React.useContext(UserContext);
};

export const UserContextProvider = ({ children }) => {
  const { isLoading, data, error, refetch } = useQuery("user", () =>
    fetch("/api/user")
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") return data.payload;
        else return null;
      })
  );

  const userContextValue = {
    reloadUser: refetch,
    user: isLoading || error ? null : data,
    isLoading: isLoading,
  };

  return (
    <UserContext.Provider value={userContextValue}>
      {children}
    </UserContext.Provider>
  );
};
