import { createContext, useContext, useState, useEffect } from "react";

// Create a "box" to hold login info that any component can read.
const AuthContext = createContext(null);

// Custom hook so pages can easily access auth data: useAuth()
export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}

// Wraps the whole app and keeps track of who is logged in.
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // On first page load, check if we saved a login in localStorage.
  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");
    const username = localStorage.getItem("username");
    const isStudent = localStorage.getItem("is_student");

    if (accessToken && username !== null) {
      setUser({
        username: username,
        isStudent: isStudent === "true",
      });
      setIsAuthenticated(true);
    }
  }, []);

  // Called after a successful login API response.
  function login(accessToken, refreshToken, username, isStudent) {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
    localStorage.setItem("username", username);
    localStorage.setItem("is_student", String(isStudent));

    setUser({ username, isStudent });
    setIsAuthenticated(true);
  }

  // Clear everything when the user clicks Logout.
  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");
    localStorage.removeItem("is_student");

    setUser(null);
    setIsAuthenticated(false);
  }

  const value = {
    user,
    isAuthenticated,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
