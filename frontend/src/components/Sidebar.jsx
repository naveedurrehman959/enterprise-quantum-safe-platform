import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ROLE_PERMISSIONS } from "../utils/roles";

const menuItems = [
  { name: "Dashboard", path: "/dashboard" },
  { name: "Analytics", path: "/analytics" },

  { name: "Asset Discovery", path: "/discovery" },
  { name: "Inventory", path: "/inventory" },
  { name: "Risk Assessment", path: "/risk" },
  { name: "Policy Engine", path: "/policy" },
  { name: "Crypto Agility", path: "/crypto-agility" },
  { name: "Migration Engine", path: "/migration" },

  { name: "PKI", path: "/pki" },
  { name: "Compliance", path: "/compliance" },
  { name: "Monitoring", path: "/monitoring" },
  { name: "Audit Logs", path: "/audit" },
  { name: "Notifications", path: "/notifications" },

  { name: "Search", path: "/search" },
  { name: "Reports", path: "/reports" },

  { name: "Profile", path: "/profile" },
  { name: "Settings", path: "/settings" },
];
function Sidebar() {
  const { user } = useAuth();

  const permissions =
    ROLE_PERMISSIONS[user?.role] || [];

  const visibleItems =
    permissions.includes("*")
      ? menuItems
      : menuItems.filter((item) =>
          permissions.includes(item.path)
        );

  return (
    <aside
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "250px",
        height: "100vh",
        background: "#172554",
        color: "#fff",
        overflowY: "auto",
        padding: "20px 0",
        boxSizing: "border-box",
      }}
    >
      <h2
        style={{
          textAlign: "center",
          marginBottom: "20px",
        }}
      >
        Quantum-Safe
      </h2>

      <hr
        style={{
          borderColor: "#334155",
          marginBottom: "15px",
        }}
      />

      {visibleItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          style={({ isActive }) => ({
            display: "block",
            padding: "12px 20px",
            textDecoration: "none",
            color: "#fff",
            background: isActive
              ? "#2563eb"
              : "transparent",
            borderLeft: isActive
              ? "4px solid #60a5fa"
              : "4px solid transparent",
          })}
        >
          {item.name}
        </NavLink>
      ))}
    </aside>
  );
}

export default Sidebar;
