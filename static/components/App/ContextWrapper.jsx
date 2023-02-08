import React from "react";
import { QueryClient, QueryClientProvider } from "react-query";

import { UserContextProvider } from "../../context/UserContext";

const queryClient = new QueryClient();

const ContextWrapper = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <UserContextProvider>{children}</UserContextProvider>
    </QueryClientProvider>
  );
};

export default ContextWrapper;
