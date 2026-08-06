import { useState } from "react";
import { useNavigate } from "react-router-dom";
import notify from "../utils/notify";
import { useAuth } from "../context/AuthContext";

function Login() {

    const navigate = useNavigate();

    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [loading, setLoading] = useState(false);

    const handleLogin = async () => {

        try {

            setLoading(true);

            await login(email, password);

            notify.success("Login successful");
            navigate("/dashboard");

        } catch {

            notify.error("Invalid email or password");

        } finally {

            setLoading(false);

        }

    };

    return (

        <div
            style={{
                height: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                flexDirection: "column",
                gap: "12px",
            }}
        >

            <h1>Enterprise Quantum-Safe Platform</h1>

            <input
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button
                disabled={loading}
                onClick={handleLogin}
            >
                {loading ? "Signing In..." : "Login"}
            </button>

        </div>

    );

}

export default Login;
