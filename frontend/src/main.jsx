import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import "./index.css";
import App from "./App";
import { AuthProvider } from "./context/AuthContext";

ReactDOM.createRoot(
    document.getElementById("root")
).render(

    <BrowserRouter>

        <AuthProvider>

            <Toaster
                position="top-right"
                reverseOrder={false}
                toastOptions={{
                    duration: 3000,
                    style: {
                        fontSize: "14px",
                        borderRadius: "10px"
                    }
                }}
            />

            <App />

        </AuthProvider>

    </BrowserRouter>

);
