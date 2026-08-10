
import { useCallback, useEffect, useState } from "react";

import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  Divider,
  Button,
  TextField,
  Stack,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from "@mui/material";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import VerifiedIcon from "@mui/icons-material/Verified";

import migrationService from "../services/migrationService";
import policyService from "../services/policyService";

function MigrationEngine() {
  const [loading, setLoading] = useState(true);

  const [status, setStatus] = useState({});
  const [report, setReport] = useState({});
  const [policy, setPolicy] = useState({});

  const [algorithm, setAlgorithm] = useState("RSA-2048");

  const [analysis, setAnalysis] = useState(null);
  const [plan, setPlan] = useState(null);

  /*
   * ============================================================
   * Load Migration Engine Data
   * ============================================================
   */

  const loadData = useCallback(async () => {
    try {
      setLoading(true);

      const [policyRes, statusRes, reportRes] =
        await Promise.all([
          policyService.getStatus(),
          migrationService.getStatus(),
          migrationService.getReport(),
        ]);

      setPolicy(policyRes.data || {});
      setStatus(statusRes.data || {});
      setReport(reportRes.data || {});
    } catch (error) {
      console.error(
        "Migration Engine data loading failed:",
        error
      );
    } finally {
      setLoading(false);
    }
  }, []);

  /*
   * ============================================================
   * Initial Load
   * ============================================================
   */

  useEffect(() => {
    const loadInitialData = async () => {
      await loadData();
    };

    loadInitialData();
  }, [loadData]);

  /*
   * ============================================================
   * Migration Analysis
   * ============================================================
   */

  const analyze = async () => {
    try {
      const response =
        await migrationService.analyze(algorithm);

      setAnalysis(response.data || null);
    } catch (error) {
      console.error(
        "Migration analysis failed:",
        error
      );
    }
  };

  /*
   * ============================================================
   * Generate Migration Plan
   * ============================================================
   */

  const generatePlan = async () => {
    try {
      const response =
        await migrationService.createPlan(
          algorithm
        );

      setPlan(response.data || null);
    } catch (error) {
      console.error(
        "Migration plan generation failed:",
        error
      );
    }
  };

  /*
   * ============================================================
   * Loading State
   * ============================================================
   */

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

  /*
   * ============================================================
   * Dashboard
   * ============================================================
   */

  return (
    <Box>
      <Typography
        variant="h4"
        fontWeight="bold"
        gutterBottom
      >
        Migration Engine
      </Typography>

      <Typography
        color="text.secondary"
        mb={4}
      >
        Enterprise Post-Quantum Cryptography Migration Center
      </Typography>

      {/* ======================================================
          Metrics
          ====================================================== */}

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="Engine"
            value={status.status || "UNKNOWN"}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="Module"
            value={report.module || "Migration Engine"}
          />
        </Grid>

        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="Compliance"
            value={
              report.compliance?.length || 0
            }
          />
        </Grid>

        <Grid size={{ xs: 12, md: 3 }}>
          <MetricCard
            title="Supported Algorithms"
            value={
              report.supported_algorithms?.length || 0
            }
          />
        </Grid>
      </Grid>

      {/* ======================================================
          Migration Status + Security Policy
          ====================================================== */}

      <Grid
        container
        spacing={3}
        sx={{ mt: 1 }}
      >
        <Grid size={{ xs: 12, md: 6 }}>
          <Card>
            <CardContent>
              <Typography
                variant="h6"
                gutterBottom
              >
                Migration Status
              </Typography>

              <Divider sx={{ mb: 2 }} />

              <Typography>
                Status:

                <Chip
                  sx={{ ml: 1 }}
                  color="success"
                  label={
                    status.status || "UNKNOWN"
                  }
                  size="small"
                />
              </Typography>

              <Typography mt={2}>
                Progress
              </Typography>

              <LinearProgress
                variant="determinate"
                value={75}
                sx={{ mt: 1 }}
              />

              <Typography
                mt={3}
                gutterBottom
              >
                Supported Modes
              </Typography>

              <Stack
                direction="row"
                spacing={1}
                flexWrap="wrap"
                useFlexGap
              >
                {status.supported_modes?.map(
                  (mode) => (
                    <Chip
                      key={mode}
                      label={mode}
                      color="primary"
                    />
                  )
                )}
              </Stack>

              <Typography
                mt={3}
                gutterBottom
              >
                Target Algorithms
              </Typography>

              <Stack
                direction="row"
                spacing={1}
                flexWrap="wrap"
                useFlexGap
              >
                {status.target_algorithms?.map(
                  (algo) => (
                    <Chip
                      key={algo}
                      color="success"
                      label={algo}
                    />
                  )
                )}
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 6 }}>
          <Card>
            <CardContent>
              <Typography
                variant="h6"
                gutterBottom
              >
                Security Policy
              </Typography>

              <Divider sx={{ mb: 2 }} />

              <Typography mb={1}>
                Allowed Algorithms
              </Typography>

              <Stack
                direction="row"
                spacing={1}
                flexWrap="wrap"
                useFlexGap
              >
                {policy.allowed_algorithms?.map(
                  (item) => (
                    <Chip
                      key={item}
                      color="success"
                      label={item}
                    />
                  )
                )}
              </Stack>

              <Typography
                mt={3}
                mb={1}
              >
                Blocked Algorithms
              </Typography>

              <Stack
                direction="row"
                spacing={1}
                flexWrap="wrap"
                useFlexGap
              >
                {policy.blocked_algorithms?.map(
                  (item) => (
                    <Chip
                      key={item}
                      color="error"
                      label={item}
                    />
                  )
                )}
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* ======================================================
          Migration Analysis
          ====================================================== */}

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography
            variant="h6"
            gutterBottom
          >
            Migration Analysis
          </Typography>

          <Divider sx={{ mb: 3 }} />

          <Stack
            direction={{ xs: "column", sm: "row" }}
            spacing={2}
          >
            <TextField
              label="Algorithm"
              value={algorithm}
              onChange={(event) =>
                setAlgorithm(event.target.value)
              }
              sx={{
                width: {
                  xs: "100%",
                  sm: 300,
                },
              }}
            />

            <Button
              variant="contained"
              onClick={analyze}
            >
              Analyze
            </Button>

            <Button
              variant="outlined"
              onClick={generatePlan}
            >
              Generate Plan
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {/* ======================================================
          Analysis Result
          ====================================================== */}

      {analysis && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography
              variant="h6"
              gutterBottom
            >
              Analysis Result
            </Typography>

            <Divider sx={{ mb: 2 }} />

            <Grid container spacing={2}>
              <Grid size={{ xs: 12, md: 4 }}>
                <MetricCard
                  title="Risk Score"
                  value={
                    analysis.risk_score ?? "N/A"
                  }
                />
              </Grid>

              <Grid size={{ xs: 12, md: 4 }}>
                <MetricCard
                  title="Risk Level"
                  value={
                    analysis.risk_level || "N/A"
                  }
                />
              </Grid>

              <Grid size={{ xs: 12, md: 4 }}>
                <MetricCard
                  title="Migration"
                  value={
                    analysis.migration_required
                      ? "Required"
                      : "Not Required"
                  }
                />
              </Grid>
            </Grid>

            <Typography
              mt={3}
              fontWeight="bold"
            >
              Recommendation
            </Typography>

            <Typography>
              {analysis.recommendation ||
                "No recommendation available."}
            </Typography>

            <Typography
              mt={2}
              fontWeight="bold"
            >
              Recommended Algorithms
            </Typography>

            <Stack
              direction="row"
              spacing={1}
              mt={1}
              flexWrap="wrap"
              useFlexGap
            >
              {Array.isArray(
                analysis.recommended_algorithm
              ) &&
                analysis.recommended_algorithm.map(
                  (item) => (
                    <Chip
                      key={item}
                      color="success"
                      label={item}
                    />
                  )
                )}
            </Stack>
          </CardContent>
        </Card>
      )}

      {/* ======================================================
          Migration Plan
          ====================================================== */}

      {plan && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography
              variant="h6"
              gutterBottom
            >
              Migration Plan
            </Typography>

            <Divider sx={{ mb: 2 }} />

            <List>
              {plan.migration_steps?.map(
                (step, index) => (
                  <ListItem
                    key={`${step}-${index}`}
                  >
                    <ListItemIcon>
                      <ArrowForwardIcon color="primary" />
                    </ListItemIcon>

                    <ListItemText
                      primary={step}
                    />
                  </ListItem>
                )
              )}
            </List>
          </CardContent>
        </Card>
      )}

      {/* ======================================================
          Compliance + Platform Features
          ====================================================== */}

      <Grid
        container
        spacing={3}
        sx={{ mt: 2 }}
      >
        <Grid size={{ xs: 12, md: 6 }}>
          <Card>
            <CardContent>
              <Typography
                variant="h6"
                gutterBottom
              >
                Compliance Standards
              </Typography>

              <Divider sx={{ mb: 2 }} />

              <Stack spacing={1}>
                {report.compliance?.map(
                  (item) => (
                    <Chip
                      key={item}
                      icon={<VerifiedIcon />}
                      label={item}
                      color="success"
                    />
                  )
                )}
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, md: 6 }}>
          <Card>
            <CardContent>
              <Typography
                variant="h6"
                gutterBottom
              >
                Platform Features
              </Typography>

              <Divider sx={{ mb: 2 }} />

              <List>
                {report.features?.map(
                  (item) => (
                    <ListItem key={item}>
                      <ListItemIcon>
                        <CheckCircleIcon color="primary" />
                      </ListItemIcon>

                      <ListItemText
                        primary={item}
                      />
                    </ListItem>
                  )
                )}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

function MetricCard({ title, value }) {
  return (
    <Card
      elevation={3}
      sx={{
        height: "100%",
      }}
    >
      <CardContent>
        <Typography
          color="text.secondary"
        >
          {title}
        </Typography>

        <Typography
          variant="h5"
          fontWeight="bold"
          mt={1}
        >
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default MigrationEngine;


