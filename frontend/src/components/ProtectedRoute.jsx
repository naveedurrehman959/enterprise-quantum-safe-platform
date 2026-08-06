import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function ProtectedRoute({ children, roles = [] }) {
  const { user } = useAuth();

  const token = localStorage.getItem("access_token");

  if (!token || !user) {
    return <Navigate to="/" replace />;
  }

  if (
    roles.length > 0 &&
    !roles.includes(user.role)
  ) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <h1>403</h1>
        <h2>Access Denied</h2>
        <p>
          You don't have permission to access this page.
        </p>
      </div>
    );
  }

  return children;
}

export default ProtectedRoute;
