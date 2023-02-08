import React, { useEffect, useState } from "react";

const UserContext = React.createContext({});

export const useUser = () => {
  return React.useContext(UserContext);
};

export const UserContextProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/api/user")
      .then((response) => response.json())
      .then((data) => {
        if (!data) return;
        if (data.status !== "success") setUser(null);
        else setUser(data.payload);
      });
  }, [userId]);

  const userContextValue = {
    setUserId: setUserId,
    user: user,
  };

  return (
    <UserContext.Provider value={userContextValue}>
      {children}
    </UserContext.Provider>
  );
};
