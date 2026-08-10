import { useState } from "react";
import AuthContext from "./authContext";
import { login as loginAPI } from "../services/authService";

export function AuthProvider({ children }) {
    const [user, setUser] = useState(
        JSON.parse(localStorage.getItem("user")) || null
    );

    const login = async (email, password) => {
        const data = await loginAPI(email, password);

        localStorage.setItem(
            "access_token",
            data.access_token
        );

        localStorage.setItem(
            "refresh_token",
            data.refresh_token
        );

        const userData = {
            username: data.username,
            role: data.role
        };

        localStorage.setItem(
            "user",
            JSON.stringify(userData)
        );

        setUser(userData);

        return data;
    };

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");

        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                login,
                logout
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}
