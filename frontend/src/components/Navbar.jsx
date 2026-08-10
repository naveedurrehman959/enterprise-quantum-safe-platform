import { Box, Typography, Avatar, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";
function Navbar() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/", { replace: true });
  };

  return (
    <Box
      sx={{
        position: "fixed",
        top: 0,
        left: "250px",
        right: 0,
        height: "70px",
        bgcolor: "#fff",
        borderBottom: "1px solid #e5e7eb",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        px: 4,
        zIndex: 1100,
        boxShadow: "0 2px 8px rgba(0,0,0,.05)",
      }}
    >
      <Typography
        variant="h5"
        fontWeight="bold"
        color="primary"
      >
        Enterprise Quantum-Safe Platform
      </Typography>

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 2,
        }}
      >
        <Typography>
          {user?.username}
        </Typography>

        <Typography
          sx={{
            color: "#64748b",
            fontSize: 14,
          }}
        >
          ({user?.role})
        </Typography>

        <Avatar>
          {user?.username?.charAt(0).toUpperCase()}
        </Avatar>

        <Button
          variant="contained"
          color="error"
          onClick={handleLogout}
        >
          Logout
        </Button>
      </Box>
    </Box>
  );
}

export default Navbar;
