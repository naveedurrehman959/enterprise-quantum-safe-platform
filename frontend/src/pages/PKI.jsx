import { useEffect, useState } from "react";

import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Stack,
  Divider,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
  Select,
  MenuItem,
} from "@mui/material";

import { DataGrid } from "@mui/x-data-grid";

import VerifiedIcon from "@mui/icons-material/Verified";
import ShieldIcon from "@mui/icons-material/Shield";
import LockIcon from "@mui/icons-material/Lock";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import DeleteForeverIcon from "@mui/icons-material/DeleteForever";
import AddIcon from "@mui/icons-material/Add";

import pkiService from "../services/pkiService";

function PKI() {

  const [loading, setLoading] = useState(true);

  const [certificates, setCertificates] = useState([]);

  const [dialogOpen, setDialogOpen] = useState(false);

  const [type, setType] = useState("PQC-SERVER");

  const [algorithm, setAlgorithm] = useState("ML-DSA-65");

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success",
  });

  useEffect(() => {
    loadCertificates();
  }, []);

  const loadCertificates = async () => {

    try {

      const response =
        await pkiService.getCertificates();

      setCertificates(
        response.data.certificates || []
      );

    } catch (error) {

      console.error(error);

    }

    setLoading(false);

  };

  const issueCertificate = async () => {

    try {

      await pkiService.issueCertificate({
        type,
        algorithm,
      });

      setDialogOpen(false);

      await loadCertificates();

      setSnackbar({
        open: true,
        severity: "success",
        message: "Certificate issued successfully.",
      });

    } catch (error) {

      console.error(error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "Certificate issuance failed.",
      });

    }

  };

  const revokeCertificate = async (serial) => {

    try {

      await pkiService.revokeCertificate(serial);

      await loadCertificates();

      setSnackbar({
        open: true,
        severity: "success",
        message: "Certificate revoked successfully.",
      });

    } catch (error) {

      console.error(error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "Unable to revoke certificate.",
      });

    }

  };

  if (loading) {

    return (

      <Box
        display="flex"
        justifyContent="center"
        mt={10}
      >
        <CircularProgress />
      </Box>

    );

  }

  const totalCertificates =
    certificates.length;

  const activeCertificates =
    certificates.filter(
      c => c.status === "active"
    ).length;

  const revokedCertificates =
    certificates.filter(
      c => c.status === "revoked"
    ).length;

  const pqcCertificates =
    certificates.filter(
      c => c.algorithm?.includes("ML")
    ).length;

  const riskyCertificates =
    certificates.filter(
      c => c.quantum_risk !== "SAFE"
    ).length;

  const columns = [

    {
      field: "id",
      headerName: "ID",
      width: 80,
    },

    {
      field: "type",
      headerName: "Certificate Type",
      flex: 1,
    },

    {
      field: "algorithm",
      headerName: "Algorithm",
      flex: 1,

      renderCell: (params) => (

        <Chip
          label={params.value || "Unknown"}
          color={
            params.value?.includes("ML")
              ? "success"
              : "warning"
          }
          size="small"
        />

      ),

    },

    {
      field: "quantum_risk",
      headerName: "Quantum Risk",
      width: 150,

      renderCell: (params) => (

        <Chip
          label={params.value || "UNKNOWN"}
          color={
            params.value === "SAFE"
              ? "success"
              : params.value === "LOW"
              ? "info"
              : "error"
          }
          size="small"
        />

      ),

    },

    {
      field: "status",
      headerName: "Status",
      width: 140,

      renderCell: (params) => (

        <Chip
          label={params.value}
          color={
            params.value === "active"
              ? "success"
              : "default"
          }
          size="small"
        />

      ),

    },

    {
      field: "migration_status",
      headerName: "Migration",
      width: 160,

      renderCell: (params) => (

        <Chip
          label={params.value || "Pending"}
          color={
            params.value === "Completed"
              ? "success"
              : "warning"
          }
          size="small"
        />

      ),

    },

    {
      field: "action",
      headerName: "Action",
      width: 170,
      sortable: false,

      renderCell: (params) => (

        <Button
          color="error"
          size="small"
          startIcon={<DeleteForeverIcon />}
          onClick={() =>
            revokeCertificate(params.row.serial)
          }
        >
          Revoke
        </Button>

      ),

    },

  ];

   return (

    <Box>

      <Typography
        variant="h4"
        fontWeight="bold"
        gutterBottom
      >
        Enterprise PKI Management
      </Typography>

      <Typography
        color="text.secondary"
        mb={4}
      >
        Certificate Authority, Post-Quantum Certificates,
        Lifecycle Management and Crypto-Agility
      </Typography>

      <Grid
        container
        spacing={3}
      >

        <Grid size={{ xs: 12, md: 2.4 }}>
          <MetricCard
            title="Certificates"
            value={totalCertificates}
            icon={<VerifiedIcon />}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 2.4 }}>
          <MetricCard
            title="Active"
            value={activeCertificates}
            icon={<ShieldIcon />}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 2.4 }}>
          <MetricCard
            title="PQC"
            value={pqcCertificates}
            icon={<LockIcon />}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 2.4 }}>
          <MetricCard
            title="Quantum Risk"
            value={riskyCertificates}
            icon={<WarningAmberIcon />}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 2.4 }}>
          <MetricCard
            title="Revoked"
            value={revokedCertificates}
            icon={<DeleteForeverIcon />}
          />
        </Grid>

      </Grid>

      <Grid
        container
        spacing={3}
        sx={{ mt: 1 }}
      >

        <Grid size={{ xs: 12, md: 4 }}>

          <Card>

            <CardContent>

              <Typography
                variant="h6"
                gutterBottom
              >
                Certificate Authority
              </Typography>

              <Divider sx={{ mb:2 }} />

              <Stack spacing={2}>

                <Chip
                  label="CA Status : Healthy"
                  color="success"
                />

                <Chip
                  label="Root CA : Active"
                  color="primary"
                />

                <Chip
                  label="NIST PQC Ready"
                  color="secondary"
                />

                <Chip
                  label={`Issued Certificates : ${totalCertificates}`}
                  color="info"
                />

              </Stack>

              <Divider sx={{ my:3 }} />

              <Typography
                variant="body2"
                color="text.secondary"
              >
                Enterprise PKI enables secure certificate
                lifecycle management using NIST standardized
                ML-DSA algorithms for quantum-safe identity
                protection.
              </Typography>

            </CardContent>

          </Card>

        </Grid>

        <Grid size={{ xs:12, md:8 }}>

          <Card>

            <CardContent>

              <Stack
                direction="row"
                justifyContent="space-between"
                alignItems="center"
                mb={2}
              >

                <Typography variant="h6">
                  Certificate Inventory
                </Typography>

                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() =>
                    setDialogOpen(true)
                  }
                >
                  Issue Certificate
                </Button>

              </Stack>

              <Divider sx={{ mb:2 }} />

              <Box
                sx={{
                  height:520
                }}
              >

                <DataGrid

                  rows={certificates}

                  columns={columns}

                  pageSizeOptions={[5,10]}

                  disableRowSelectionOnClick

                />

              </Box>

            </CardContent>

          </Card>

        </Grid>

      </Grid>


      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >

        <DialogTitle>

          Issue Post-Quantum Certificate

        </DialogTitle>

        <DialogContent>

          <Typography
            color="text.secondary"
            sx={{ mb: 3 }}
          >

            Generate enterprise-ready certificates using
            NIST standardized ML-DSA algorithms.

          </Typography>

          <Typography
            variant="subtitle2"
            gutterBottom
          >
            Certificate Type
          </Typography>

          <Select
            fullWidth
            value={type}
            onChange={(e) =>
              setType(e.target.value)
            }
            sx={{ mb: 3 }}
          >

            <MenuItem value="PQC-SERVER">
              PQC Server Certificate
            </MenuItem>

            <MenuItem value="PQC-CLIENT">
              PQC Client Certificate
            </MenuItem>

          </Select>

          <Typography
            variant="subtitle2"
            gutterBottom
          >
            Signature Algorithm
          </Typography>

          <Select
            fullWidth
            value={algorithm}
            onChange={(e) =>
              setAlgorithm(e.target.value)
            }
          >

            <MenuItem value="ML-DSA-44">
              ML-DSA-44
            </MenuItem>

            <MenuItem value="ML-DSA-65">
              ML-DSA-65
            </MenuItem>

            <MenuItem value="ML-DSA-87">
              ML-DSA-87
            </MenuItem>

          </Select>

        </DialogContent>

        <DialogActions>

          <Button
            onClick={() =>
              setDialogOpen(false)
            }
          >
            Cancel
          </Button>

          <Button
            variant="contained"
            onClick={issueCertificate}
          >
            Issue Certificate
          </Button>

        </DialogActions>

      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() =>
          setSnackbar({
            ...snackbar,
            open: false,
          })
        }
      >

        <Alert
          severity={snackbar.severity}
          variant="filled"
        >

          {snackbar.message}

        </Alert>

      </Snackbar>

    </Box>

  );

}

function MetricCard({

  title,

  value,

  icon,

}) {

  return (

    <Card
      elevation={3}
      sx={{
        height: "100%",
      }}
    >

      <CardContent>

        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >

          <Box>

            <Typography
              color="text.secondary"
              variant="body2"
            >
              {title}
            </Typography>

            <Typography
              variant="h4"
              fontWeight="bold"
              mt={1}
            >
              {value}
            </Typography>

          </Box>

          <Box
            sx={{
              color: "primary.main",
            }}
          >
            {icon}
          </Box>

        </Stack>

      </CardContent>

    </Card>

  );

}

export default PKI;


