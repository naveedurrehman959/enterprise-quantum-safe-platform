import { Navigate, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { ROLE_PERMISSIONS } from "../utils/roles";

function RoleRoute({ children }) {

    const { user } = useAuth();
    const location = useLocation();

    if (!user) {
        return <Navigate to="/" replace />;
    }

    const permissions =
        ROLE_PERMISSIONS[user.role] || [];

    if (permissions.includes("*")) {
        return children;
    }

    if (!permissions.includes(location.pathname)) {
        return (
            <Navigate
                to="/dashboard"
                replace
            />
        );
    }

    return children;
}

export default RoleRoute;
