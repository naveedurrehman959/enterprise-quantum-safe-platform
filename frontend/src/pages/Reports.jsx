import { useEffect, useState } from "react";

import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Divider,
  CircularProgress,
  Chip,
  Stack,
  Snackbar,
  Alert,
  LinearProgress,
} from "@mui/material";

import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import TableViewIcon from "@mui/icons-material/TableView";
import RefreshIcon from "@mui/icons-material/Refresh";
import AssessmentIcon from "@mui/icons-material/Assessment";
import SecurityIcon from "@mui/icons-material/Security";
import VerifiedUserIcon from "@mui/icons-material/VerifiedUser";
import Inventory2Icon from "@mui/icons-material/Inventory2";

import ReportCharts from "../components/charts/ReportCharts";
import reportService from "../services/reportService";

function Reports() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  const [snackbar, setSnackbar] = useState({
    open: false,
    severity: "success",
    message: "",
  });

  /*
   * ============================================================
   * Load Reports
   * ============================================================
   *
   * The async function is created inside useEffect so the effect
   * does not directly call a function that performs setState().
   */
  useEffect(() => {
    let cancelled = false;

    const fetchReports = async () => {
      try {
        if (!cancelled) {
          setLoading(true);
        }

        const [
          summary,
          risk,
          compliance,
          migration,
          audit,
          certificates,
        ] = await Promise.all([
          reportService.getSummary(),
          reportService.getRiskReport(),
          reportService.getComplianceReport(),
          reportService.getMigrationReport(),
          reportService.getAuditReport(),
          reportService.getCertificateReport(),
        ]);

        if (cancelled) {
          return;
        }

        setData({
          summary: summary.data || {},
          risk: risk.data || {},
          compliance: compliance.data || {},
          migration: migration.data || {},
          audit: audit.data || {},
          certificates: certificates.data || {},
        });
      } catch (error) {
        console.error("Reports loading failed:", error);

        if (!cancelled) {
          setSnackbar({
            open: true,
            severity: "error",
            message: "Unable to load reports.",
          });
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchReports();

    return () => {
      cancelled = true;
    };
  }, []);

  /*
   * ============================================================
   * Manual Refresh
   * ============================================================
   */
  const refreshReports = async () => {
    try {
      setLoading(true);

      const [
        summary,
        risk,
        compliance,
        migration,
        audit,
        certificates,
      ] = await Promise.all([
        reportService.getSummary(),
        reportService.getRiskReport(),
        reportService.getComplianceReport(),
        reportService.getMigrationReport(),
        reportService.getAuditReport(),
        reportService.getCertificateReport(),
      ]);

      setData({
        summary: summary.data || {},
        risk: risk.data || {},
        compliance: compliance.data || {},
        migration: migration.data || {},
        audit: audit.data || {},
        certificates: certificates.data || {},
      });

      setSnackbar({
        open: true,
        severity: "success",
        message: "Reports refreshed successfully.",
      });
    } catch (error) {
      console.error("Reports refresh failed:", error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "Unable to refresh reports.",
      });
    } finally {
      setLoading(false);
    }
  };

  /*
   * ============================================================
   * Export PDF
   * ============================================================
   */
  const downloadPDF = async () => {
    try {
      const response = await reportService.exportPDF();

      const blob = new Blob([response.data], {
        type: "application/pdf",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "Enterprise-Quantum-Report.pdf";

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);

      setSnackbar({
        open: true,
        severity: "success",
        message: "PDF exported successfully.",
      });
    } catch (error) {
      console.error("PDF export failed:", error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "PDF export failed.",
      });
    }
  };

  /*
   * ============================================================
   * Export CSV
   * ============================================================
   */
  const downloadCSV = async () => {
    try {
      const response = await reportService.exportCSV();

      const blob = new Blob([response.data], {
        type: "text/csv",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "Enterprise-Quantum-Report.csv";

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);

      setSnackbar({
        open: true,
        severity: "success",
        message: "CSV exported successfully.",
      });
    } catch (error) {
      console.error("CSV export failed:", error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "CSV export failed.",
      });
    }
  };

  /*
   * ============================================================
   * Loading State
   * ============================================================
   */
  if (loading && !data) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="50vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  /*
   * ============================================================
   * Error State
   * ============================================================
   */
  if (!data) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="40vh"
      >
        <Alert severity="error">
          Unable to load report data.
        </Alert>
      </Box>
    );
  }

  const migration = data.migration || {};
  const risk = data.risk || {};
  const compliance = data.compliance || {};
  const audit = data.audit || {};
  const summary = data.summary || {};
  const certificates = data.certificates || {};

  const totalAssets = Number(migration.total_assets || 0);
  const migratedAssets = Number(migration.migrated_assets || 0);

  const completion =
    totalAssets > 0
      ? Math.min((migratedAssets / totalAssets) * 100, 100)
      : 0;

  const complianceStatus =
    compliance.status || "UNKNOWN";

  const complianceHealthy = [
    "Healthy",
    "ACTIVE",
    "PASS",
    "Compliant",
  ].includes(complianceStatus);

  return (
    <Box>
      {/* ============================================================
          Header
          ============================================================ */}

      <Stack
        direction={{
          xs: "column",
          md: "row",
        }}
        justifyContent="space-between"
        alignItems={{
          xs: "flex-start",
          md: "center",
        }}
        spacing={2}
        mb={4}
      >
        <Box>
          <Typography
            variant="h4"
            fontWeight="bold"
          >
            Enterprise Reports Dashboard
          </Typography>

          <Typography color="text.secondary">
            Security posture, compliance, migration analytics
            and executive reporting
          </Typography>
        </Box>

        <Stack
          direction={{
            xs: "column",
            sm: "row",
          }}
          spacing={2}
          width={{
            xs: "100%",
            md: "auto",
          }}
        >
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={refreshReports}
            disabled={loading}
          >
            {loading ? "Refreshing..." : "Refresh"}
          </Button>

          <Button
            variant="contained"
            startIcon={<PictureAsPdfIcon />}
            onClick={downloadPDF}
          >
            Export PDF
          </Button>

          <Button
            variant="contained"
            color="success"
            startIcon={<TableViewIcon />}
            onClick={downloadCSV}
          >
            Export CSV
          </Button>
        </Stack>
      </Stack>

      {/* ============================================================
          Charts
          ============================================================ */}

      <ReportCharts
        migration={migration}
        risk={risk}
        audit={audit}
      />

      {/* ============================================================
          Executive Summary
          ============================================================ */}

      <Box
        sx={{
          mt: 4,
          mb: 4,
          p: 3,
          borderRadius: 3,
          bgcolor: "background.paper",
          boxShadow: 2,
        }}
      >
        <Typography
          variant="h6"
          fontWeight="bold"
          gutterBottom
        >
          Executive Summary
        </Typography>

        <Typography
          color="text.secondary"
          sx={{ mb: 3 }}
        >
          Overall enterprise security posture generated from
          the Risk Assessment, Compliance, PKI and Migration
          engines.
        </Typography>

        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 3 }}>
            <Chip
              color={
                complianceHealthy
                  ? "success"
                  : "warning"
              }
              label={`Compliance : ${complianceStatus}`}
              sx={{
                width: "100%",
              }}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <Chip
              color="primary"
              label={`Migration : ${completion.toFixed(1)}%`}
              sx={{
                width: "100%",
              }}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <Chip
              color={
                Number(risk.critical_risk || 0) > 0
                  ? "error"
                  : "success"
              }
              label={`Critical Risks : ${
                risk.critical_risk || 0
              }`}
              sx={{
                width: "100%",
              }}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>
            <Chip
              color="secondary"
              label={`Audit Events : ${
                audit.total_events || 0
              }`}
              sx={{
                width: "100%",
              }}
            />
          </Grid>
        </Grid>
      </Box>

      {/* ============================================================
          KPI Cards
          ============================================================ */}

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="Enterprise Assets"
            value={summary.total_assets || 0}
            subtitle="Managed Assets"
            icon={
              <Inventory2Icon color="primary" />
            }
          />
        </Grid>

        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="Critical Risks"
            value={risk.critical_risk || 0}
            subtitle="Immediate Attention"
            icon={
              <SecurityIcon color="error" />
            }
          />
        </Grid>

        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="PQC Certificates"
            value={
              certificates.pqc_certificates || 0
            }
            subtitle="Quantum Safe"
            icon={
              <VerifiedUserIcon color="success" />
            }
          />
        </Grid>

        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="Audit Events"
            value={audit.total_events || 0}
            subtitle="Recorded Events"
            icon={
              <AssessmentIcon color="warning" />
            }
          />
        </Grid>

        {/* ============================================================
            Compliance
            ============================================================ */}

        <Grid size={{ xs: 12, md: 4 }}>
          <ReportCard title="Compliance Overview">
            <Typography sx={{ mb: 2 }}>
              Overall Status:
              <strong> {complianceStatus}</strong>
            </Typography>

            {Array.isArray(compliance.frameworks) &&
              compliance.frameworks.map(
                (framework) => (
                  <Chip
                    key={framework}
                    label={framework}
                    color="success"
                    sx={{
                      mr: 1,
                      mb: 1,
                    }}
                  />
                )
              )}
          </ReportCard>
        </Grid>

        {/* ============================================================
            Migration
            ============================================================ */}

        <Grid size={{ xs: 12, md: 4 }}>
          <ReportCard title="Migration Progress">
            <Typography gutterBottom>
              Migration Completion
            </Typography>

            <LinearProgress
              variant="determinate"
              value={completion}
              sx={{
                height: 10,
                borderRadius: 5,
              }}
            />

            <Typography sx={{ mt: 2 }}>
              {completion.toFixed(1)}%
            </Typography>

            <Divider sx={{ my: 2 }} />

            <Typography>
              Migrated Assets:
              <strong>
                {" "}
                {migration.migrated_assets || 0}
              </strong>
            </Typography>

            <Typography>
              Pending Assets:
              <strong>
                {" "}
                {migration.pending_assets || 0}
              </strong>
            </Typography>

            <Typography>
              Total Assets:
              <strong>
                {" "}
                {migration.total_assets || 0}
              </strong>
            </Typography>
          </ReportCard>
        </Grid>

        {/* ============================================================
            Certificates
            ============================================================ */}

        <Grid size={{ xs: 12, md: 4 }}>
          <ReportCard title="Certificate Summary">
            <Typography>
              PQC Certificates:
              <strong>
                {" "}
                {certificates.pqc_certificates || 0}
              </strong>
            </Typography>

            <Typography>
              Classical Certificates:
              <strong>
                {" "}
                {certificates.classical_certificates || 0}
              </strong>
            </Typography>

            <Typography>
              Total Certificates:
              <strong>
                {" "}
                {certificates.total_certificates || 0}
              </strong>
            </Typography>
          </ReportCard>
        </Grid>

        {/* ============================================================
            Risk
            ============================================================ */}

        <Grid size={{ xs: 12, md: 6 }}>
          <ReportCard title="Risk Summary">
            <Stack
              direction="row"
              justifyContent="space-between"
              sx={{ mb: 1 }}
            >
              <Typography>
                Critical Risks
              </Typography>

              <Chip
                label={risk.critical_risk || 0}
                color="error"
                size="small"
              />
            </Stack>

            <Typography>
              High:
              <strong>
                {" "}
                {risk.high_risk || 0}
              </strong>
            </Typography>

            <Typography>
              Medium:
              <strong>
                {" "}
                {risk.medium_risk || 0}
              </strong>
            </Typography>

            <Typography>
              Safe Assets:
              <strong>
                {" "}
                {risk.safe_assets || 0}
              </strong>
            </Typography>

            <Typography>
              Total Assets:
              <strong>
                {" "}
                {risk.total_assets || 0}
              </strong>
            </Typography>
          </ReportCard>
        </Grid>

        {/* ============================================================
            Audit
            ============================================================ */}

        <Grid size={{ xs: 12, md: 6 }}>
          <ReportCard title="Audit Summary">
            <Typography>
              Successful Events:
              <strong>
                {" "}
                {audit.successful_events || 0}
              </strong>
            </Typography>

            <Typography>
              Failed Events:
              <strong>
                {" "}
                {audit.failed_events || 0}
              </strong>
            </Typography>

            <Typography>
              Total Events:
              <strong>
                {" "}
                {audit.total_events || 0}
              </strong>
            </Typography>
          </ReportCard>
        </Grid>
      </Grid>

      {/* ============================================================
          Snackbar
          ============================================================ */}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() =>
          setSnackbar((current) => ({
            ...current,
            open: false,
          }))
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

/*
 * ================================================================
 * Metric Card
 * ================================================================
 */

function MetricCard({
  title,
  value,
  subtitle,
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

            <Typography
              variant="body2"
              color="text.secondary"
            >
              {subtitle}
            </Typography>
          </Box>

          {icon}
        </Stack>
      </CardContent>
    </Card>
  );
}

/*
 * ================================================================
 * Report Card
 * ================================================================
 */

function ReportCard({
  title,
  children,
}) {
  return (
    <Card
      elevation={3}
      sx={{
        height: "100%",
      }}
    >
      <CardContent>
        <Typography
          variant="h6"
          fontWeight="bold"
        >
          {title}
        </Typography>

        <Divider sx={{ my: 2 }} />

        {children}
      </CardContent>
    </Card>
  );
}

export default Reports;
