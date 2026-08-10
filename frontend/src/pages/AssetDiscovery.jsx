import { useEffect, useState } from "react";

import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import RefreshIcon from "@mui/icons-material/Refresh";
import DeleteIcon from "@mui/icons-material/Delete";
import SecurityIcon from "@mui/icons-material/Security";
import WarningIcon from "@mui/icons-material/Warning";
import SwapHorizIcon from "@mui/icons-material/SwapHoriz";
import StorageIcon from "@mui/icons-material/Storage";

import assetDiscoveryService from "../services/assetDiscoveryService";


function StatCard({ title, value, icon }) {
  return (
    <Paper
      elevation={2}
      sx={{
        p: 2.5,
        borderRadius: 2,
        height: "100%",
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Box>
          <Typography
            variant="body2"
            color="text.secondary"
          >
            {title}
          </Typography>

          <Typography
            variant="h4"
            sx={{
              fontWeight: 700,
              mt: 0.5,
            }}
          >
            {value}
          </Typography>
        </Box>

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: 48,
            height: 48,
            borderRadius: 2,
            backgroundColor: "#eff6ff",
            color: "#2563eb",
          }}
        >
          {icon}
        </Box>
      </Box>
    </Paper>
  );
}


function RiskChip({ risk }) {

  const value = String(risk || "UNKNOWN").toUpperCase();

  let color = "default";

  if (value === "CRITICAL") {
    color = "error";
  } else if (value === "HIGH") {
    color = "warning";
  } else if (
    value === "LOW" ||
    value === "SAFE"
  ) {
    color = "success";
  }

  return (
    <Chip
      label={value}
      color={color}
      size="small"
    />
  );
}


function PolicyChip({ decision }) {

  const value =
    String(decision || "UNKNOWN").toUpperCase();

  let color = "default";

  if (value === "MIGRATION_REQUIRED") {
    color = "warning";
  } else if (value === "BLOCK") {
    color = "error";
  } else if (
    value === "ALLOW" ||
    value === "APPROVE"
  ) {
    color = "success";
  }

  return (
    <Chip
      label={value.replaceAll("_", " ")}
      color={color}
      size="small"
    />
  );
}


function AssetDiscovery() {

  const [assets, setAssets] = useState([]);

  const [target, setTarget] = useState("");
  const [port, setPort] = useState(443);

  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [actionId, setActionId] = useState(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  const loadAssets = async () => {

    try {

      setError("");

      const data =
        await assetDiscoveryService.getAssets();

      setAssets(
        Array.isArray(data)
          ? data
          : []
      );

    } catch (err) {

      console.error(err);

      setError(
        "Failed to load discovered assets."
      );

    } finally {

      setLoading(false);

    }
  };

  useEffect(() => {
    const load = async () => {
        await loadAssets();
    };

    load();
  }, []);
  
  const handleScan = async () => {

    if (!target.trim()) {

      setError(
        "Please enter a hostname or domain."
      );

      return;

    }

    try {

      setScanning(true);
      setError("");
      setSuccess("");

      await assetDiscoveryService.scanAsset(
        target.trim(),
        port
      );

      setTarget("");

      setSuccess(
        "Asset discovered successfully."
      );

      await loadAssets();

    } catch (err) {

      console.error(err);

      setError(
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        "Asset discovery scan failed."
      );

    } finally {

      setScanning(false);

    }
  };


  const handleRescan = async (id) => {

    try {

      setActionId(id);
      setError("");
      setSuccess("");

      await assetDiscoveryService.rescanAsset(id);

      setSuccess(
        "Asset rescanned successfully."
      );

      await loadAssets();

    } catch (err) {

      console.error(err);

      setError(
        err?.response?.data?.error ||
        "Asset rescan failed."
      );

    } finally {

      setActionId(null);

    }
  };


  const handleDelete = async (id) => {

    const confirmed =
      window.confirm(
        "Delete this discovered asset?"
      );

    if (!confirmed) {
      return;
    }

    try {

      setActionId(id);
      setError("");
      setSuccess("");

      await assetDiscoveryService.deleteAsset(id);

      setSuccess(
        "Asset deleted successfully."
      );

      await loadAssets();

    } catch (err) {

      console.error(err);

      setError(
        err?.response?.data?.error ||
        "Failed to delete asset."
      );

    } finally {

      setActionId(null);

    }
  };


  const totalAssets =
    assets.length;


  const highRiskAssets =
    assets.filter(
      (asset) =>
        asset.risk_level === "HIGH" ||
        asset.risk_level === "CRITICAL"
    ).length;


  const migrationAssets =
    assets.filter(
      (asset) =>
        asset.migration_required === true
    ).length;


  const safeAssets =
    assets.filter(
      (asset) =>
        asset.risk_level === "SAFE" ||
        asset.risk_level === "LOW"
    ).length;


  return (

    <Box>

      {/* Header */}

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
          flexWrap: "wrap",
          gap: 2,
        }}
      >

        <Box>

          <Typography
            variant="h4"
            sx={{ fontWeight: 700 }}
          >
            Asset Discovery
          </Typography>

          <Typography
            color="text.secondary"
            sx={{ mt: 0.5 }}
          >
            Discover and assess cryptographic assets
            across your infrastructure.
          </Typography>

        </Box>

        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={loadAssets}
          disabled={loading}
        >
          Refresh
        </Button>

      </Box>


      {/* Alerts */}

      {error && (
        <Alert
          severity="error"
          sx={{ mb: 2 }}
          onClose={() => setError("")}
        >
          {error}
        </Alert>
      )}


      {success && (
        <Alert
          severity="success"
          sx={{ mb: 2 }}
          onClose={() => setSuccess("")}
        >
          {success}
        </Alert>
      )}


      {/* Scan */}

      <Paper
        elevation={2}
        sx={{
          p: 3,
          mb: 3,
          borderRadius: 2,
        }}
      >

        <Typography
          variant="h6"
          sx={{
            fontWeight: 600,
            mb: 2,
          }}
        >
          Discover New Asset
        </Typography>


        <Grid
          container
          spacing={2}
          alignItems="center"
        >

          <Grid size={{ xs: 12, md: 7 }}>

            <TextField
              fullWidth
              label="Hostname / Domain"
              placeholder="example.com"
              value={target}
              onChange={(e) =>
                setTarget(e.target.value)
              }
              onKeyDown={(e) => {

                if (e.key === "Enter") {
                  handleScan();
                }

              }}
            />

          </Grid>


          <Grid size={{ xs: 12, sm: 4, md: 2 }}>

            <TextField
              fullWidth
              type="number"
              label="Port"
              value={port}
              onChange={(e) =>
                setPort(e.target.value)
              }
            />

          </Grid>


          <Grid size={{ xs: 12, sm: 8, md: 3 }}>

            <Button
              fullWidth
              variant="contained"
              size="large"
              startIcon={
                scanning
                  ? <CircularProgress
                      size={20}
                      color="inherit"
                    />
                  : <SearchIcon />
              }
              onClick={handleScan}
              disabled={scanning}
              sx={{
                height: 56,
              }}
            >
              {scanning
                ? "Scanning..."
                : "Scan Asset"}
            </Button>

          </Grid>

        </Grid>

      </Paper>


      {/* Statistics */}

      <Grid
        container
        spacing={2}
        sx={{ mb: 3 }}
      >

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard
            title="Total Assets"
            value={totalAssets}
            icon={<StorageIcon />}
          />
        </Grid>


        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard
            title="High / Critical Risk"
            value={highRiskAssets}
            icon={<WarningIcon />}
          />
        </Grid>


        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard
            title="Migration Required"
            value={migrationAssets}
            icon={<SwapHorizIcon />}
          />
        </Grid>


        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard
            title="Safe Assets"
            value={safeAssets}
            icon={<SecurityIcon />}
          />
        </Grid>

      </Grid>


      {/* Asset Table */}

      <Paper
        elevation={2}
        sx={{
          borderRadius: 2,
          overflow: "hidden",
        }}
      >

        <Box
          sx={{
            p: 2.5,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >

          <Box>

            <Typography
              variant="h6"
              sx={{ fontWeight: 600 }}
            >
              Discovered Assets
            </Typography>

            <Typography
              variant="body2"
              color="text.secondary"
            >
              TLS certificates and cryptographic
              risk information
            </Typography>

          </Box>

          <Chip
            label={`${totalAssets} Assets`}
            variant="outlined"
          />

        </Box>


        <TableContainer>

          <Table
            size="small"
            sx={{ minWidth: 1100 }}
          >

            <TableHead>

              <TableRow>

                <TableCell>
                  <strong>Asset</strong>
                </TableCell>

                <TableCell>
                  <strong>IP / Port</strong>
                </TableCell>

                <TableCell>
                  <strong>Algorithm</strong>
                </TableCell>

                <TableCell>
                  <strong>Risk</strong>
                </TableCell>

                <TableCell>
                  <strong>Policy</strong>
                </TableCell>

                <TableCell>
                  <strong>Migration</strong>
                </TableCell>

                <TableCell>
                  <strong>Recommended</strong>
                </TableCell>

                <TableCell>
                  <strong>Status</strong>
                </TableCell>

                <TableCell align="right">
                  <strong>Actions</strong>
                </TableCell>

              </TableRow>

            </TableHead>


            <TableBody>

              {loading ? (

                <TableRow>

                  <TableCell
                    colSpan={9}
                    align="center"
                    sx={{ py: 6 }}
                  >

                    <CircularProgress />

                    <Typography
                      sx={{ mt: 2 }}
                      color="text.secondary"
                    >
                      Loading discovered assets...
                    </Typography>

                  </TableCell>

                </TableRow>

              ) : assets.length === 0 ? (

                <TableRow>

                  <TableCell
                    colSpan={9}
                    align="center"
                    sx={{ py: 6 }}
                  >

                    <SearchIcon
                      sx={{
                        fontSize: 48,
                        color: "text.secondary",
                      }}
                    />

                    <Typography
                      sx={{ mt: 1 }}
                    >
                      No assets discovered yet.
                    </Typography>

                    <Typography
                      variant="body2"
                      color="text.secondary"
                    >
                      Enter a hostname above to
                      start discovery.
                    </Typography>

                  </TableCell>

                </TableRow>

              ) : (

                assets.map((asset) => (

                  <TableRow
                    key={asset.id}
                    hover
                  >

                    <TableCell>

                      <Typography
                        sx={{ fontWeight: 600 }}
                      >
                        {asset.hostname}
                      </Typography>

                      <Typography
                        variant="caption"
                        color="text.secondary"
                      >
                        {asset.subject || "TLS Asset"}
                      </Typography>

                    </TableCell>


                    <TableCell>

                      <Typography variant="body2">
                        {asset.ip_address}
                      </Typography>

                      <Typography
                        variant="caption"
                        color="text.secondary"
                      >
                        Port {asset.port}
                      </Typography>

                    </TableCell>


                    <TableCell>

                      <Chip
                        label={
                          asset.public_key_algorithm ||
                          "Unknown"
                        }
                        size="small"
                        variant="outlined"
                      />

                    </TableCell>


                    <TableCell>

                      <RiskChip
                        risk={asset.risk_level}
                      />

                      <Typography
                        variant="caption"
                        display="block"
                        color="text.secondary"
                        sx={{ mt: 0.5 }}
                      >
                        Score: {asset.risk_score ?? 0}
                      </Typography>

                    </TableCell>


                    <TableCell>

                      <PolicyChip
                        decision={
                          asset.policy_decision
                        }
                      />

                    </TableCell>


                    <TableCell>

                      {asset.migration_required ? (

                        <Chip
                          label="Required"
                          color="warning"
                          size="small"
                        />

                      ) : (

                        <Chip
                          label="Not Required"
                          color="success"
                          size="small"
                        />

                      )}

                    </TableCell>


                    <TableCell>

                      <Typography
                        variant="body2"
                        sx={{
                          fontWeight: 600,
                        }}
                      >
                        {
                          asset.recommended_algorithm ||
                          "—"
                        }
                      </Typography>

                    </TableCell>


                    <TableCell>

                      <Chip
                        label={
                          asset.scan_status ||
                          "UNKNOWN"
                        }
                        color={
                          asset.scan_status ===
                          "SUCCESS"
                            ? "success"
                            : "default"
                        }
                        size="small"
                      />

                    </TableCell>


                    <TableCell align="right">

                      <Button
                        size="small"
                        startIcon={
                          actionId === asset.id
                            ? (
                              <CircularProgress
                                size={15}
                              />
                            )
                            : <RefreshIcon />
                        }
                        onClick={() =>
                          handleRescan(asset.id)
                        }
                        disabled={
                          actionId === asset.id
                        }
                        sx={{ mr: 1 }}
                      >
                        Rescan
                      </Button>


                      <Button
                        size="small"
                        color="error"
                        startIcon={<DeleteIcon />}
                        onClick={() =>
                          handleDelete(asset.id)
                        }
                        disabled={
                          actionId === asset.id
                        }
                      >
                        Delete
                      </Button>

                    </TableCell>

                  </TableRow>

                ))

              )}

            </TableBody>

          </Table>

        </TableContainer>

      </Paper>

    </Box>
  );
}


export default AssetDiscovery;
