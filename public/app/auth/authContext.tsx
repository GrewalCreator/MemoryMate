import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthContextType {
  token: string | null;
  saveToken: (token: string) => void;
  logout: () => void;
  saveUser: (user: object) => void; // Allow saving a user object
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<object | null>(null); // Store the user as an object

  useEffect(() => {
    const loadAuthData = async () => {
      try {
        const savedToken = await AsyncStorage.getItem('token');
        const savedUser = await AsyncStorage.getItem('user');
        setToken(savedToken || null);
        setUser(savedUser ? JSON.parse(savedUser) : null); // Parse user JSON string
      } catch (error) {
        console.error('Failed to load auth data:', error);
      }
    };
    loadAuthData();
  }, []);

  const saveToken = async (token: string) => {
    try {
      await AsyncStorage.setItem('token', token);
      setToken(token);
    } catch (error) {
      console.error('Failed to save token:', error);
    }
  };

  const saveUser = async (user: object) => {
    try {
      const userString = JSON.stringify(user); // Convert user object to string
      await AsyncStorage.setItem('user', userString);
      setUser(user);
    } catch (error) {
      console.error('Failed to save user:', error);
    }
  };

  const logout = async () => {
    try {
      await AsyncStorage.removeItem('token');
      await AsyncStorage.removeItem('user');
      setToken(null);
      setUser(null);
    } catch (error) {
      console.error('Failed to log out:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ token, saveToken, logout, saveUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Add this default export
export default AuthProvider;
