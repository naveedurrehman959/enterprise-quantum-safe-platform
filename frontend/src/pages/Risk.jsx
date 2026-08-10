
import { useEffect, useState } from "react";

import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Snackbar,
  Stack,
  Typography,
} from "@mui/material";

import {
  Analytics as AnalyticsIcon,
  ArrowForward as ArrowForwardIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Security as SecurityIcon,
  Warning as WarningIcon,
  AutoFixHigh as MigrationIcon,
} from "@mui/icons-material";

import { useNavigate } from "react-router-dom";

import api from "../services/api";
import migrationService from "../services/migrationService";

function Risk() {
  const navigate = useNavigate();

  // ============================================================
  // State
  // ============================================================

  const [risk, setRisk] = useState(null);

  const [algorithm, setAlgorithm] = useState("ECDSA");

  const [analysis, setAnalysis] = useState(null);

  const [plan, setPlan] = useState(null);

  const [loading, setLoading] = useState(true);

  const [analyzing, setAnalyzing] = useState(false);

  const [generatingPlan, setGeneratingPlan] = useState(false);

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success",
  });

  // ============================================================
  // Initial Risk Assessment
  // ============================================================

  useEffect(() => {
    let cancelled = false;

    const fetchRiskAssessment = async () => {
      try {
        const response = await api.get("/risk/assessment");

        if (!cancelled) {
          setRisk(response.data);
        }
      } catch (error) {
        if (!cancelled) {
          console.error(
            "Risk assessment error:",
            error
          );

          setSnackbar({
            open: true,
            message: "Unable to load risk assessment.",
            severity: "error",
          });
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchRiskAssessment();

    return () => {
      cancelled = true;
    };
  }, []);

  // ============================================================
  // Analyze Algorithm
  // ============================================================

  const analyzeRisk = async () => {
    setAnalyzing(true);
    setPlan(null);

    try {
      const response = await api.post(
        "/risk/analyze",
        {
          algorithm,
        }
      );

      setAnalysis(response.data);

      setSnackbar({
        open: true,
        message: `${algorithm} risk analysis completed.`,
        severity: "success",
      });
    } catch (error) {
      console.error(
        "Algorithm analysis error:",
        error
      );

      setSnackbar({
        open: true,
        message: "Algorithm risk analysis failed.",
        severity: "error",
      });
    } finally {
      setAnalyzing(false);
    }
  };

  // ============================================================
  // Generate Migration Plan
  // ============================================================

  const generateMigrationPlan = async () => {
    if (!analysis) {
      return;
    }

    setGeneratingPlan(true);

    try {
      const response =
        await migrationService.createPlan(
          analysis.algorithm
        );

      setPlan(response.data);

      setSnackbar({
        open: true,
        message: "Migration plan generated successfully.",
        severity: "success",
      });
    } catch (error) {
      console.error(
        "Migration plan error:",
        error
      );

      setSnackbar({
        open: true,
        message: "Unable to generate migration plan.",
        severity: "error",
      });
    } finally {
      setGeneratingPlan(false);
    }
  };

  // ============================================================
  // Loading
  // ============================================================

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
      >
        <CircularProgress />
      </Box>
    );
  }

  // ============================================================
  // Risk Level Helpers
  // ============================================================

  const getRiskColor = (level) => {
    switch (level) {
      case "CRITICAL":
      case "HIGH":
        return "error";

      case "MEDIUM":
        return "warning";

      case "LOW":
        return "info";

      case "SAFE":
        return "success";

      default:
        return "default";
    }
  };

  const getDecisionColor = (decision) => {
    switch (decision) {
      case "APPROVED":
        return "success";

      case "MIGRATION_REQUIRED":
        return "warning";

      case "BLOCKED":
        return "error";

      default:
        return "default";
    }
  };

  // ============================================================
  // Render
  // ============================================================

  return (
    <Box>
      {/* ======================================================
          Header
      ====================================================== */}

      <Typography
        variant="h4"
        fontWeight="bold"
        gutterBottom
      >
        Risk Assessment
      </Typography>

      <Typography
        color="text.secondary"
        mb={4}
      >
        Enterprise quantum-risk analysis,
        cryptographic assessment and migration
        recommendations.
      </Typography>

      {/* ======================================================
          Risk Summary
      ====================================================== */}

      <Grid container spacing={2}>
        <MetricCard
          title="Total Assets"
          value={risk?.total_assets ?? 0}
          icon={<AnalyticsIcon />}
        />

        <MetricCard
          title="Safe Assets"
          value={risk?.safe_assets ?? 0}
          icon={<CheckCircleIcon />}
        />

        <MetricCard
          title="Medium Risk"
          value={risk?.medium_risk ?? 0}
          icon={<WarningIcon />}
        />

        <MetricCard
          title="High Risk"
          value={risk?.high_risk ?? 0}
          icon={<WarningIcon />}
        />

        <MetricCard
          title="Critical Risk"
          value={risk?.critical_risk ?? 0}
          icon={<ErrorIcon />}
        />
      </Grid>

      {/* ======================================================
          Quantum Readiness
      ====================================================== */}

      <Card
        elevation={3}
        sx={{ mt: 2 }}
      >
        <CardContent>
          <Typography
            variant="subtitle1"
            fontWeight="500"
          >
            Quantum Readiness
          </Typography>

          <Typography
            variant="h3"
            fontWeight="500"
            sx={{ mt: 1 }}
          >
            {risk?.quantum_readiness_score ?? 0}%
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
          >
            Enterprise quantum-safe readiness
            score based on current cryptographic
            inventory.
          </Typography>
        </CardContent>
      </Card>

      {/* ======================================================
          Cryptographic Risk Analysis
      ====================================================== */}

      <Card
        elevation={3}
        sx={{ mt: 2 }}
      >
        <CardContent>
          <Typography
            variant="h6"
            gutterBottom
          >
            Cryptographic Risk Analysis
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mb: 3 }}
          >
            Analyze a cryptographic algorithm
            against the enterprise quantum-risk
            database.
          </Typography>

          <Stack
            direction={{
              xs: "column",
              sm: "row",
            }}
            spacing={2}
            alignItems={{
              xs: "stretch",
              sm: "center",
            }}
          >
            <FormControl
              sx={{
                minWidth: 220,
              }}
            >
              <InputLabel>
                Algorithm
              </InputLabel>

              <Select
                value={algorithm}
                label="Algorithm"
                onChange={(event) => {
                  setAlgorithm(
                    event.target.value
                  );

                  setAnalysis(null);
                  setPlan(null);
                }}
              >
                <MenuItem value="RSA-1024">
                  RSA-1024
                </MenuItem>

                <MenuItem value="RSA-2048">
                  RSA-2048
                </MenuItem>

                <MenuItem value="RSA-4096">
                  RSA-4096
                </MenuItem>

                <MenuItem value="ECDSA">
                  ECDSA
                </MenuItem>

                <MenuItem value="ECC">
                  ECC
                </MenuItem>

                <MenuItem value="ECDHE">
                  ECDHE
                </MenuItem>

                <MenuItem value="ED25519">
                  ED25519
                </MenuItem>

                <MenuItem value="AES-128">
                  AES-128
                </MenuItem>

                <MenuItem value="AES-256-GCM">
                  AES-256-GCM
                </MenuItem>

                <MenuItem value="SHA1">
                  SHA-1
                </MenuItem>

                <MenuItem value="ML-KEM-768">
                  ML-KEM-768
                </MenuItem>

                <MenuItem value="ML-DSA-65">
                  ML-DSA-65
                </MenuItem>
              </Select>
            </FormControl>

            <Button
              variant="contained"
              startIcon={
                analyzing ? (
                  <CircularProgress
                    size={18}
                    color="inherit"
                  />
                ) : (
                  <SecurityIcon />
                )
              }
              onClick={analyzeRisk}
              disabled={analyzing}
            >
              {analyzing
                ? "Analyzing..."
                : "Analyze Risk"}
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {/* ======================================================
          Analysis Result
      ====================================================== */}

      {analysis && (
        <Card
          elevation={3}
          sx={{ mt: 2 }}
        >
          <CardContent>
            <Typography
              variant="h6"
              gutterBottom
            >
              Risk Analysis Result
            </Typography>

            <Divider sx={{ mb: 3 }} />

            <Grid container spacing={3}>
              <ResultItem
                label="Algorithm"
                value={analysis.algorithm}
              />

              <ResultItem
                label="Risk Score"
                value={`${analysis.risk_score} / 100`}
              />

              <Grid
                size={{
                  xs: 12,
                  sm: 6,
                  md: 3,
                }}
              >
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Risk Level
                </Typography>

                <Box sx={{ mt: 1 }}>
                  <Chip
                    icon={
                      analysis.risk_level ===
                      "SAFE" ? (
                        <CheckCircleIcon />
                      ) : (
                        <WarningIcon />
                      )
                    }
                    label={
                      analysis.risk_level
                    }
                    color={getRiskColor(
                      analysis.risk_level
                    )}
                  />
                </Box>
              </Grid>

              <Grid
                size={{
                  xs: 12,
                  sm: 6,
                  md: 3,
                }}
              >
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Decision
                </Typography>

                <Box sx={{ mt: 1 }}>
                  <Chip
                    label={
                      analysis.decision
                    }
                    color={getDecisionColor(
                      analysis.decision
                    )}
                  />
                </Box>
              </Grid>

              <ResultItem
                label="Quantum Vulnerable"
                value={
                  analysis.quantum_vulnerable
                    ? "YES"
                    : "NO"
                }
              />

              <ResultItem
                label="Migration Required"
                value={
                  analysis.migration_required
                    ? "YES"
                    : "NO"
                }
              />
            </Grid>

            <Box sx={{ mt: 3 }}>
              <Alert
                severity={
                  analysis.migration_required
                    ? "warning"
                    : "success"
                }
              >
                <strong>
                  Recommendation:
                </strong>{" "}
                {analysis.recommendation}
              </Alert>
            </Box>

            <Box sx={{ mt: 3 }}>
              <Typography
                variant="caption"
                color="text.secondary"
              >
                Recommended Algorithm
              </Typography>

              <Typography
                variant="h6"
                sx={{ mt: 0.5 }}
              >
                {analysis.recommended_algorithm ||
                  "No migration required"}
              </Typography>
            </Box>

            {analysis.migration_required && (
              <Box sx={{ mt: 3 }}>
                <Divider sx={{ mb: 3 }} />

                <Stack
                  direction={{
                    xs: "column",
                    sm: "row",
                  }}
                  spacing={2}
                >
                  <Button
                    variant="contained"
                    color="warning"
                    startIcon={
                      generatingPlan ? (
                        <CircularProgress
                          size={18}
                          color="inherit"
                        />
                      ) : (
                        <MigrationIcon />
                      )
                    }
                    endIcon={
                      !generatingPlan && (
                        <ArrowForwardIcon />
                      )
                    }
                    onClick={
                      generateMigrationPlan
                    }
                    disabled={generatingPlan}
                  >
                    {generatingPlan
                      ? "Generating Plan..."
                      : "Generate Migration Plan"}
                  </Button>

                  <Button
                    variant="outlined"
                    onClick={() =>
                      navigate("/migration")
                    }
                  >
                    Open Migration Engine
                  </Button>
                </Stack>
              </Box>
            )}
          </CardContent>
        </Card>
      )}

      {/* ======================================================
          Migration Plan
      ====================================================== */}

      {plan && (
        <Card
          elevation={3}
          sx={{ mt: 2 }}
        >
          <CardContent>
            <Stack
              direction={{
                xs: "column",
                sm: "row",
              }}
              justifyContent="space-between"
              alignItems={{
                xs: "flex-start",
                sm: "center",
              }}
              spacing={2}
            >
              <Box>
                <Typography
                  variant="h6"
                  gutterBottom
                >
                  Migration Plan
                </Typography>

                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Generated by the Enterprise
                  Migration Engine.
                </Typography>
              </Box>

              <Chip
                label={
                  plan.status ||
                  "READY_FOR_MIGRATION"
                }
                color="success"
              />
            </Stack>

            <Divider sx={{ my: 3 }} />

            <Grid container spacing={3}>
              <ResultItem
                label="Source Algorithm"
                value={
                  plan.source_algorithm ||
                  analysis?.algorithm
                }
              />

              <ResultItem
                label="Algorithm Category"
                value={
                  plan.algorithm_category ||
                  "Cryptographic Algorithm"
                }
              />

              <ResultItem
                label="Target Algorithm"
                value={
                  Array.isArray(
                    plan.target_algorithm
                  )
                    ? plan.target_algorithm.join(
                        ", "
                      )
                    : plan.target_algorithm ||
                      analysis?.recommended_algorithm ||
                      "PQC Migration"
                }
              />
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Typography
                variant="subtitle1"
                fontWeight="bold"
                gutterBottom
              >
                Migration Steps
              </Typography>

              <Stack spacing={1.5}>
                {(plan.migration_steps || []).map(
                  (step, index) => (
                    <Paper
                      key={index}
                      variant="outlined"
                      sx={{
                        p: 2,
                        display: "flex",
                        alignItems: "center",
                        gap: 2,
                      }}
                    >
                      <Chip
                        label={index + 1}
                        size="small"
                        color="primary"
                      />

                      <Typography>
                        {step}
                      </Typography>
                    </Paper>
                  )
                )}
              </Stack>
            </Box>

            <Alert
              severity="success"
              icon={<MigrationIcon />}
              sx={{ mt: 3 }}
            >
              Migration plan is ready for
              implementation.
            </Alert>

            <Box sx={{ mt: 3 }}>
              <Button
                variant="outlined"
                startIcon={<MigrationIcon />}
                onClick={() =>
                  navigate("/migration")
                }
              >
                Continue in Migration Engine
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* ======================================================
          Snackbar
      ====================================================== */}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3500}
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
          onClose={() =>
            setSnackbar({
              ...snackbar,
              open: false,
            })
          }
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}

// ============================================================
// Metric Card
// ============================================================

function MetricCard({
  title,
  value,
  icon,
}) {
  return (
    <Grid
      size={{
        xs: 12,
        sm: 6,
        md: 2.4,
      }}
    >
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
                variant="body2"
                color="text.secondary"
              >
                {title}
              </Typography>

              <Typography
                variant="h5"
                fontWeight="bold"
                sx={{ mt: 0.5 }}
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
    </Grid>
  );
}

// ============================================================
// Result Item
// ============================================================

function ResultItem({
  label,
  value,
}) {
  return (
    <Grid
      size={{
        xs: 12,
        sm: 6,
        md: 3,
      }}
    >
      <Typography
        variant="caption"
        color="text.secondary"
      >
        {label}
      </Typography>

      <Typography
        variant="body1"
        fontWeight="500"
        sx={{ mt: 0.5 }}
      >
        {value}
      </Typography>
    </Grid>
  );
}

export default Risk;


