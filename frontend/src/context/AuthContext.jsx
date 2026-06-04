
import { createContext, useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const savedToken = sessionStorage.getItem('ah_token');
    if (savedToken) {
      setToken(savedToken);
      authService.getMe()
        .then((userData) => setUser(userData))
        .catch(() => {
          sessionStorage.removeItem('ah_token');
          setToken(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    const response = await authService.login(email, password);
    sessionStorage.setItem('ah_token', response.access_token);
    setToken(response.access_token);
    setUser(response.user);
    return response;
  }, []);

  const register = useCallback(async (data) => {
    const response = await authService.register(data);
    return response;
  }, []);

  const logout = useCallback(() => {
    sessionStorage.removeItem('ah_token');
    setToken(null);
    setUser(null);
  }, []);

  const value = {
    user,
    token,
    isLoading,
    isAuthenticated: !!token,
    role: user?.role || null,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
