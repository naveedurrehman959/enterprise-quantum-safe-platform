import { Routes, Route, Navigate } from "react-router-dom";

import AssetDiscovery from "./pages/AssetDiscovery";
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

      {/* =====================================================
          PUBLIC ROUTES
      ====================================================== */}

      <Route
        path="/"
        element={<Login />}
      />


      {/* =====================================================
          PROTECTED APPLICATION
      ====================================================== */}

      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >

        {/* =================================================
            GENERAL
        ================================================== */}

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/profile"
          element={<Profile />}
        />


        {/* =================================================
            ANALYTICS
        ================================================== */}

        <Route
          path="/analytics"
          element={
            <RoleRoute>
              <Analytics />
            </RoleRoute>
          }
        />


        {/* =================================================
            ASSET DISCOVERY
        ================================================== */}

        <Route
          path="/discovery"
          element={
            <RoleRoute>
              <AssetDiscovery />
            </RoleRoute>
          }
        />


        {/* =================================================
            CRYPTOGRAPHIC INVENTORY
        ================================================== */}

        <Route
          path="/inventory"
          element={
            <RoleRoute>
              <Inventory />
            </RoleRoute>
          }
        />


        {/* =================================================
            CRYPTO POLICY ENGINE
        ================================================== */}

        <Route
          path="/policy"
          element={
            <RoleRoute>
              <Policy />
            </RoleRoute>
          }
        />


        {/* =================================================
            RISK ASSESSMENT
        ================================================== */}

        <Route
          path="/risk"
          element={
            <RoleRoute>
              <Risk />
            </RoleRoute>
          }
        />


        {/* =================================================
            MIGRATION ENGINE
        ================================================== */}

        <Route
          path="/migration"
          element={
            <RoleRoute>
              <MigrationEngine />
            </RoleRoute>
          }
        />


        {/* =================================================
            CRYPTO AGILITY
        ================================================== */}

        <Route
          path="/crypto-agility"
          element={
            <RoleRoute>
              <CryptoAgility />
            </RoleRoute>
          }
        />


        {/* =================================================
            VAULT / KEY MANAGEMENT
        ================================================== */}

        <Route
          path="/vault"
          element={
            <RoleRoute>
              <Vault />
            </RoleRoute>
          }
        />


        {/* =================================================
            PKI
        ================================================== */}

        <Route
          path="/pki"
          element={
            <RoleRoute>
              <PKI />
            </RoleRoute>
          }
        />


        {/* =================================================
            COMPLIANCE
        ================================================== */}

        <Route
          path="/compliance"
          element={
            <RoleRoute>
              <Compliance />
            </RoleRoute>
          }
        />


        {/* =================================================
            MONITORING
        ================================================== */}

        <Route
          path="/monitoring"
          element={
            <RoleRoute>
              <Monitoring />
            </RoleRoute>
          }
        />


        {/* =================================================
            NOTIFICATIONS
        ================================================== */}

        <Route
          path="/notifications"
          element={
            <RoleRoute>
              <Notifications />
            </RoleRoute>
          }
        />


        {/* =================================================
            REPORTING
        ================================================== */}

        <Route
          path="/reports"
          element={
            <RoleRoute>
              <Reports />
            </RoleRoute>
          }
        />


        {/* =================================================
            AUDIT LOGS
        ================================================== */}

        <Route
          path="/audit"
          element={
            <RoleRoute>
              <AuditLogs />
            </RoleRoute>
          }
        />


        {/* =================================================
            SEARCH
        ================================================== */}

        <Route
          path="/search"
          element={
            <RoleRoute>
              <Search />
            </RoleRoute>
          }
        />


        {/* =================================================
            SETTINGS
        ================================================== */}

        <Route
          path="/settings"
          element={
            <RoleRoute>
              <Settings />
            </RoleRoute>
          }
        />

      </Route>


      {/* =====================================================
          UNKNOWN ROUTES
      ====================================================== */}

      <Route
        path="*"
        element={<Navigate to="/" replace />}
      />

    </Routes>
  );
}

export default App;
