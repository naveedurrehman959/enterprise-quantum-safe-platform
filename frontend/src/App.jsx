import { Routes, Route, Navigate } from "react-router-dom";

import Vault from "./pages/Vault";
import Login from "./pages/Login";

import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import RoleRoute from "./components/RoleRoute";

import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Search from "./pages/Search";
import Analytics from "./pages/Analytics";
import Inventory from "./pages/Inventory";
import Policy from "./pages/Policy";
import Notifications from "./pages/Notifications";
import CryptoAgility from "./pages/CryptoAgility";
import MigrationEngine from "./pages/MigrationEngine";
import Risk from "./pages/Risk";
import Reports from "./pages/Reports";
import PKI from "./pages/PKI";
import Compliance from "./pages/Compliance";
import Monitoring from "./pages/Monitoring";
import AuditLogs from "./pages/AuditLogs";
import Settings from "./pages/Settings";

function App() {
  return (
    <Routes>

      {/* Public Route */}
      <Route
        path="/"
        element={<Login />}
      />

      {/* Protected Routes */}
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >

        {/* Accessible to every authenticated user */}
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/profile"
          element={<Profile />}
        />

        {/* Role Protected Routes */}

        <Route
          path="/analytics"
          element={
            <RoleRoute>
              <Analytics />
            </RoleRoute>
          }
        />

        <Route
          path="/inventory"
          element={
            <RoleRoute>
              <Inventory />
            </RoleRoute>
          }
        />

        <Route
          path="/policy"
          element={
            <RoleRoute>
              <Policy />
            </RoleRoute>
          }
        />

        <Route
          path="/notifications"
          element={
            <RoleRoute>
              <Notifications />
            </RoleRoute>
          }
        />

        <Route
          path="/crypto-agility"
          element={
            <RoleRoute>
              <CryptoAgility />
            </RoleRoute>
          }
        />

        <Route
          path="/migration"
          element={
            <RoleRoute>
              <MigrationEngine />
            </RoleRoute>
          }
        />
        <Route
 path="/vault"
 element={<Vault/>}
/>
        <Route
          path="/risk"
          element={
            <RoleRoute>
              <Risk />
            </RoleRoute>
          }
        />

        <Route
          path="/reports"
          element={
            <RoleRoute>
              <Reports />
            </RoleRoute>
          }
        />

        <Route
          path="/pki"
          element={
            <RoleRoute>
              <PKI />
            </RoleRoute>
          }
        />

        <Route
          path="/compliance"
          element={
            <RoleRoute>
              <Compliance />
            </RoleRoute>
          }
        />

        <Route
          path="/monitoring"
          element={
            <RoleRoute>
              <Monitoring />
            </RoleRoute>
          }
        />

        <Route
          path="/audit"
          element={
            <RoleRoute>
              <AuditLogs />
            </RoleRoute>
          }
        />

        <Route
          path="/search"
          element={
            <RoleRoute>
              <Search />
            </RoleRoute>
          }
        />

        <Route
          path="/settings"
          element={
            <RoleRoute>
              <Settings />
            </RoleRoute>
          }
        />

      </Route>

      <Route
        path="*"
        element={<Navigate to="/" replace />}
      />

    </Routes>
  );
}

export default App;
