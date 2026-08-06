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

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    setLoading(true);

    try {
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
        summary: summary.data,
        risk: risk.data,
        compliance: compliance.data,
        migration: migration.data,
        audit: audit.data,
        certificates: certificates.data,
      });
    } catch (error) {
      console.error(error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "Unable to load reports.",
      });
    } finally {
      setLoading(false);
    }
  };

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
      console.error(error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "PDF export failed.",
      });
    }
  };

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
      console.error(error);

      setSnackbar({
        open: true,
        severity: "error",
        message: "CSV export failed.",
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

  if (!data) {
  return (
    <Typography color="error">
      Unable to load report data.
    </Typography>
  );
};

  const completion =
    data.migration.total_assets > 0
      ? (data.migration.migrated_assets /
          data.migration.total_assets) *
        100
      : 0;
  return (
    <Box>

      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
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
            Security posture, compliance, migration analytics and executive reporting
          </Typography>

        </Box>

        <Stack
          direction="row"
          spacing={2}
        >

          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={loadReports}
          >
            Refresh
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

      <ReportCharts
        migration={data.migration}
        risk={data.risk}
        audit={data.audit}
      />

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
          Overall enterprise security posture generated from the Risk Assessment,
          Compliance, PKI and Migration engines.
        </Typography>

        <Grid
          container
          spacing={2}
        >

          <Grid size={{ xs: 12, md: 3 }}>

            <Chip
              color={
                ["Healthy","ACTIVE","PASS","Compliant"]
                    .includes(data.compliance.status)
                  ? "success"
                  : "warning"
              }
              label={`Compliance : ${data.compliance.status}`}
              sx={{ width: "100%" }}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>

            <Chip
              color="primary"
              label={`Migration : ${completion.toFixed(1)}%`}
              sx={{ width: "100%" }}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>

            <Chip
              color={
                data.risk.critical_risk > 0
                  ? "error"
                  : "success"
              }
              label={`Critical Risks : ${data.risk.critical_risk}`}
              sx={{ width: "100%" }}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 3 }}>

            <Chip
              color="secondary"
              label={`Audit Events : ${data.audit.total_events}`}
              sx={{ width: "100%" }}
            />

          </Grid>

        </Grid>

      </Box>

      <Grid
        container
        spacing={3}
      >
      <Grid size={{ xs: 12, md: 3 }}>
        <MetricCard
          title="Enterprise Assets"
          value={data.summary.total_assets || 0}
          subtitle="Managed Assets"
          icon={<Inventory2Icon color="primary" />}
        />
      </Grid>

      <Grid size={{ xs: 12, md: 3 }}>
        <MetricCard
          title="Critical Risks"
          value={data.risk.critical_risk || 0}
          subtitle="Immediate Attention"
          icon={<SecurityIcon color="error" />}
        />
      </Grid>

      <Grid size={{ xs: 12, md: 3 }}>
        <MetricCard
          title="PQC Certificates"
          value={data.certificates.pqc_certificates || 0}
          subtitle="Quantum Safe"
          icon={<VerifiedUserIcon color="success" />}
        />
      </Grid>

      <Grid size={{ xs: 12, md: 3 }}>
        <MetricCard
          title="Audit Events"
          value={data.audit.total_events || 0}
          subtitle="Recorded Events"
          icon={<AssessmentIcon color="warning" />}
        />
      </Grid>

      <Grid size={{ xs: 12, md: 4 }}>
        <ReportCard title="Compliance Overview">

          <Typography sx={{ mb: 2 }}>
            Overall Status:
            <strong> {data.compliance.status}</strong>
          </Typography>

          {data.compliance.frameworks?.map((framework) => (
            <Chip
              key={framework}
              label={framework}
              color="success"
              sx={{ mr: 1, mb: 1 }}
            />
          ))}

        </ReportCard>
      </Grid>

      <Grid size={{ xs: 12, md: 4 }}>
        <ReportCard title="Migration Progress">

          <Typography gutterBottom>
            Migration Completion
          </Typography>

          <LinearProgress
            variant="determinate"
            value={completion}
            sx={{ height: 10, borderRadius: 5 }}
          />

          <Typography sx={{ mt: 2 }}>
            {completion.toFixed(1)}%
          </Typography>

          <Divider sx={{ my: 2 }} />

          <Typography>
            Migrated Assets:
            <strong> {data.migration.migrated_assets}</strong>
          </Typography>

          <Typography>
            Pending Assets:
            <strong> {data.migration.pending_assets}</strong>
          </Typography>

        </ReportCard>
      </Grid>

      <Grid size={{ xs: 12, md: 4 }}>
        <ReportCard title="Certificate Summary">

          <Typography>
            PQC Certificates:
            <strong> {data.certificates.pqc_certificates}</strong>
          </Typography>

          <Typography>
            Classical Certificates:
            <strong> {data.certificates.classical_certificates}</strong>
          </Typography>

          <Typography>
            Total Certificates:
            <strong> {data.certificates.total_certificates}</strong>
          </Typography>

        </ReportCard>
      </Grid>

      <Grid size={{ xs: 12, md: 6 }}>
        <ReportCard title="Risk Summary">

          <Stack
    direction="row"
    justifyContent="space-between"
    sx={{ mb: 1 }}
>
    <Typography>Critical Risks</Typography>

    <Chip
        label={data.risk.critical_risk}
        color="error"
        size="small"
    />
</Stack>

          <Typography>
            High:
            <strong> {data.risk.high_risk}</strong>
          </Typography>

          <Typography>
            Medium:
            <strong> {data.risk.medium_risk}</strong>
          </Typography>

          <Typography>
            Safe Assets:
            <strong> {data.risk.safe_assets}</strong>
          </Typography>

        </ReportCard>
      </Grid>

      <Grid size={{ xs: 12, md: 6 }}>
        <ReportCard title="Audit Summary">

          <Typography>
            Successful Events:
            <strong> {data.audit.successful_events}</strong>
          </Typography>

          <Typography>
            Failed Events:
            <strong> {data.audit.failed_events}</strong>
          </Typography>

          <Typography>
            Total Events:
            <strong> {data.audit.total_events}</strong>
          </Typography>

        </ReportCard>
      </Grid>

    </Grid>

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
  subtitle,
  icon,
}) {

  return (
    <Card elevation={3} sx={{ height: "100%" }}>
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

function ReportCard({
  title,
  children,
}) {

  return (
    <Card elevation={3} sx={{ height: "100%" }}>
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
