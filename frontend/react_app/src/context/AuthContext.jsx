import React, { createContext, useState, useEffect, useContext } from 'react';
import { loginUser, registerUser, getCurrentUser } from '../api';
import toast from 'react-hot-toast';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);

    // Check if user is logged in on mount
    useEffect(() => {
        const initAuth = async () => {
            const storedToken = localStorage.getItem('token');
            if (storedToken) {
                try {
                    // Verify token and get user info
                    // Note: We might need a specific endpoint for this or just decode if we trust it
                    // For now, let's assume if we have a token we try to fetch 'me'
                    // If the backend doesn't have a 'me' endpoint that accepts just the token header easily without 
                    // complex setup, we might skip this or implement it. 
                    // Looking at auth.py, there is /auth/me

                    // We need to configure api.js to send the token. 
                    // For now, we'll just set the token state. 
                    // Real validation happens when we make a request.
                    setToken(storedToken);

                    // Optional: Fetch user details immediately
                    // const userData = await getCurrentUser(storedToken);
                    // setUser(userData);
                } catch (error) {
                    console.error("Auth init error", error);
                    logout();
                }
            }
            setLoading(false);
        };

        initAuth();
    }, []);

    const login = async (email, password) => {
        try {
            const data = await loginUser({ email, password });
            if (data.success) {
                setToken(data.access_token);
                setUser(data.user); // Assuming login returns user info too, or we fetch it
                localStorage.setItem('token', data.access_token);
                toast.success('Giriş başarılı!');
                return true;
            }
            return false;
        } catch (error) {
            console.error("Login error", error);
            toast.error(error.message || 'Giriş başarısız');
            throw error;
        }
    };

    const register = async (userData) => {
        try {
            const data = await registerUser(userData);
            if (data.success) {
                // Auto login after register? Or just redirect to login?
                // Let's auto login if the backend returns a token, otherwise ask to login
                if (data.access_token) {
                    setToken(data.access_token);
                    setUser(data.user);
                    localStorage.setItem('token', data.access_token);
                    toast.success('Kayıt başarılı! Hoşgeldiniz.');
                } else {
                    toast.success('Kayıt başarılı! Lütfen giriş yapın.');
                }
                return true;
            }
            return false;
        } catch (error) {
            console.error("Register error", error);
            toast.error(error.message || 'Kayıt başarısız');
            throw error;
        }
    };

    const logout = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('token');
        toast.success('Çıkış yapıldı');
    };

    const value = {
        user,
        token,
        isAuthenticated: !!token,
        login,
        register,
        logout,
        loading
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
