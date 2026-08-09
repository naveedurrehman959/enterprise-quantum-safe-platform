import { useEffect, useState } from "react";

import {
  Grid,
  Paper,
  Typography,
  Chip,
  Box,
  Alert,
  CircularProgress,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  Button,
} from "@mui/material";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import BlockIcon from "@mui/icons-material/Block";
import SecurityIcon from "@mui/icons-material/Security";

import DashboardCard from "../components/DashboardCard";

import policyService from "../services/policyService";

function Policy() {
  const [policy, setPolicy] = useState(null);
  const [error, setError] = useState("");

  const [localPolicies, setLocalPolicies] = useState([]);

  const [saving, setSaving] = useState(null);

  useEffect(() => {
    loadPolicy();
  }, []);

  /*
   * ==========================================
   * Load Policy
   * ==========================================
   */

  const loadPolicy = async () => {
    try {
      setError("");

      const response = await policyService.getStatus();

      const data = response.data;

      setPolicy(data);

      /*
       * Backend may eventually return:
       *
       * policies: [
       *   {
       *     algorithm_name: "RSA-2048",
       *     enabled: true,
       *     deployment_mode: "HYBRID",
       *     enforcement_action: "MIGRATE"
       *   }
       * ]
       *
       * For now we also support the existing
       * approved_algorithms / blocked_algorithms
       * response.
       */

      if (Array.isArray(data.policies)) {
        setLocalPolicies(data.policies);
      } else {
        const approved = data.approved_algorithms || [];
        const blocked = data.blocked_algorithms || [];
        const active = data.active_algorithms || [];

        const algorithmMap = {};

        approved.forEach((algorithm) => {
          algorithmMap[algorithm] = {
            algorithm_name: algorithm,
            enabled: active.includes(algorithm),
            deployment_mode: "CLASSICAL",
            enforcement_action: "ALLOW",
          };
        });

        blocked.forEach((algorithm) => {
          if (!algorithmMap[algorithm]) {
            algorithmMap[algorithm] = {
              algorithm_name: algorithm,
              enabled: active.includes(algorithm),
              deployment_mode: "CLASSICAL",
              enforcement_action: "BLOCK",
            };
          }
        });

        setLocalPolicies(
          Object.values(algorithmMap)
        );
      }
    } catch (error) {
      console.error(
        "Policy Engine error:",
        error
      );

      setError(
        error.response?.data?.message ||
          error.response?.data?.error ||
          "Unable to load Cryptographic Policy Engine."
      );
    }
  };

  /*
   * ==========================================
   * Update Local Policy
   * ==========================================
   */

  const updateLocalPolicy = (
    algorithmName,
    field,
    value
  ) => {
    setLocalPolicies((currentPolicies) =>
      currentPolicies.map((item) =>
        item.algorithm_name === algorithmName
          ? {
              ...item,
              [field]: value,
            }
          : item
      )
    );
  };

  /*
   * ==========================================
   * Save Policy
   * ==========================================
   *
   * Current backend supports:
   *
   * PUT /policy/algorithm/<id>
   *
   * with:
   *
   * {
   *   "allowed": true/false
   * }
   *
   * Therefore the enforcement action is mapped
   * to allowed/blocked for now.
   *
   * Full deployment_mode and enforcement_action
   * persistence will be connected after the
   * backend policy API is upgraded.
   */
const savePolicy = async (item) => {
  try {
    setSaving(item.algorithm_name);
    setError("");

    await policyService.updatePolicy(
      item.algorithm_name,
      {
        enabled: item.enabled,
        deployment_mode: item.deployment_mode,
        enforcement_action: item.enforcement_action,
      }
    );

    // Reload from backend so the UI shows
    // the actual persisted policy.
    await loadPolicy();

  } catch (error) {
    console.error("Policy update error:", error);

    setError(
      error.response?.data?.message ||
        error.response?.data?.error ||
        error.message ||
        "Unable to save policy."
    );
  } finally {
    setSaving(null);
  }
};

  /*
   * ==========================================
   * Loading
   * ==========================================
   */

  if (!policy && !error) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="300px"
      >
        <CircularProgress />
      </Box>
    );
  }

  /*
   * ==========================================
   * Error
   * ==========================================
   */

  if (error && !policy) {
    return (
      <Box>
        <Typography
          variant="h4"
          fontWeight="bold"
          sx={{ mb: 1 }}
        >
          Cryptographic Policy Engine
        </Typography>

        <Typography
          color="text.secondary"
          sx={{ mb: 3 }}
        >
          Enterprise cryptographic security policy,
          algorithm enforcement and quantum-safe
          compliance.
        </Typography>

        <Alert severity="error">
          {error}
        </Alert>
      </Box>
    );
  }

  /*
   * ==========================================
   * Policy Data
   * ==========================================
   */

  const approvedAlgorithms =
    policy.approved_algorithms ||
    policy.allowed_algorithms ||
    [];

  const blockedAlgorithms =
    policy.blocked_algorithms ||
    [];

  const conditionalAlgorithms =
    policy.conditional_algorithms ||
    [];

  const policyStatus =
    policy.status ||
    policy.policy_status ||
    "ACTIVE";

  /*
   * ==========================================
   * UI
   * ==========================================
   */

  return (
    <Box>

      {/* =======================================
          Page Header
          ======================================= */}

      <Typography
        variant="h4"
        fontWeight="bold"
        sx={{ mb: 1 }}
      >
        Cryptographic Policy Engine
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mb: 3 }}
      >
        Enterprise cryptographic security policy,
        algorithm enforcement and quantum-safe
        compliance.
      </Typography>

      {error && (
        <Alert
          severity="error"
          sx={{ mb: 3 }}
        >
          {error}
        </Alert>
      )}

      {/* =======================================
          Summary Cards
          ======================================= */}

      <Grid
        container
        spacing={3}
        sx={{ mb: 3 }}
      >

        <Grid
          size={{
            xs: 12,
            sm: 6,
            md: 3,
          }}
        >
          <DashboardCard
            title="Policy Status"
            value={policyStatus}
          />
        </Grid>

        <Grid
          size={{
            xs: 12,
            sm: 6,
            md: 3,
          }}
        >
          <DashboardCard
            title="Approved Algorithms"
            value={approvedAlgorithms.length}
          />
        </Grid>

        <Grid
          size={{
            xs: 12,
            sm: 6,
            md: 3,
          }}
        >
          <DashboardCard
            title="Blocked Algorithms"
            value={blockedAlgorithms.length}
          />
        </Grid>

        <Grid
          size={{
            xs: 12,
            sm: 6,
            md: 3,
          }}
        >
          <DashboardCard
            title="Conditional Algorithms"
            value={conditionalAlgorithms.length}
          />
        </Grid>

      </Grid>

      {/* =======================================
          Algorithm Policy Configuration
          ======================================= */}

      <Grid
        container
        spacing={3}
        sx={{ mb: 3 }}
      >

        <Grid size={{ xs: 12 }}>

          <Paper
            elevation={3}
            sx={{
              p: 3,
              borderRadius: 2,
            }}
          >

            <Typography
              variant="h6"
              gutterBottom
            >
              Algorithm Policy Configuration
            </Typography>

            <Typography
              color="text.secondary"
              sx={{ mb: 3 }}
            >
              Configure which cryptographic algorithms
              are permitted, blocked, or require
              migration.
            </Typography>

            {localPolicies.length === 0 ? (

              <Alert severity="info">
                No algorithm policies are currently
                available.
              </Alert>

            ) : (

              localPolicies.map((item) => (

                <Paper
                  key={item.algorithm_name}
                  variant="outlined"
                  sx={{
                    p: 2,
                    mb: 2,
                  }}
                >

                  <Grid
                    container
                    spacing={2}
                    alignItems="center"
                  >

                    {/* Algorithm */}

                    <Grid
                      size={{
                        xs: 12,
                        md: 3,
                      }}
                    >

                      <Typography
                        fontWeight="bold"
                      >
                        {item.algorithm_name}
                      </Typography>

                    </Grid>

                    {/* Deployment Mode */}

                    <Grid
                      size={{
                        xs: 12,
                        sm: 6,
                        md: 2.5,
                      }}
                    >

                      <FormControl
                        fullWidth
                        size="small"
                      >

                        <InputLabel>
                          Mode
                        </InputLabel>

                        <Select
                          value={
                            item.deployment_mode ||
                            "CLASSICAL"
                          }
                          label="Mode"
                          onChange={(event) =>
                            updateLocalPolicy(
                              item.algorithm_name,
                              "deployment_mode",
                              event.target.value
                            )
                          }
                        >

                          <MenuItem value="CLASSICAL">
                            Classical
                          </MenuItem>

                          <MenuItem value="HYBRID">
                            Hybrid
                          </MenuItem>

                          <MenuItem value="PURE_PQC">
                            Pure PQC
                          </MenuItem>

                        </Select>

                      </FormControl>

                    </Grid>

                    {/* Enforcement Action */}

                    <Grid
                      size={{
                        xs: 12,
                        sm: 6,
                        md: 2.5,
                      }}
                    >

                      <FormControl
                        fullWidth
                        size="small"
                      >

                        <InputLabel>
                          Action
                        </InputLabel>

                        <Select
                          value={
                            item.enforcement_action ||
                            "BLOCK"
                          }
                          label="Action"
                          onChange={(event) =>
                            updateLocalPolicy(
                              item.algorithm_name,
                              "enforcement_action",
                              event.target.value
                            )
                          }
                        >

                          <MenuItem value="ALLOW">
                            Allow
                          </MenuItem>

                          <MenuItem value="BLOCK">
                            Block
                          </MenuItem>

                          <MenuItem value="MIGRATE">
                            Migrate
                          </MenuItem>

                          <MenuItem value="REVIEW">
                            Manual Review
                          </MenuItem>

                        </Select>

                      </FormControl>

                    </Grid>

                    {/* Enabled */}

                    <Grid
                      size={{
                        xs: 12,
                        sm: 6,
                        md: 1.5,
                      }}
                    >

                      <Box
                        display="flex"
                        alignItems="center"
                      >

                        <Switch
                          checked={Boolean(
                            item.enabled
                          )}
                          onChange={(event) =>
                            updateLocalPolicy(
                              item.algorithm_name,
                              "enabled",
                              event.target.checked
                            )
                          }
                        />

                        <Typography>
                          {item.enabled
                            ? "Enabled"
                            : "Disabled"}
                        </Typography>

                      </Box>

                    </Grid>

                    {/* Save */}

                    <Grid
                      size={{
                        xs: 12,
                        sm: 6,
                        md: 2.5,
                      }}
                    >

                      <Button
                        fullWidth
                        variant="contained"
                        onClick={() =>
                          savePolicy(item)
                        }
                        disabled={
                          saving ===
                          item.algorithm_name
                        }
                      >

                        {saving ===
                        item.algorithm_name ? (

                          <CircularProgress
                            size={22}
                            color="inherit"
                          />

                        ) : (

                          "Save Policy"

                        )}

                      </Button>

                    </Grid>

                  </Grid>

                </Paper>

              ))

            )}

          </Paper>

        </Grid>

      </Grid>

      {/* =======================================
          Policy Status
          ======================================= */}

      <Grid
        container
        spacing={3}
      >

        <Grid size={{ xs: 12 }}>

          <Paper
            elevation={3}
            sx={{
              p: 3,
              borderRadius: 2,
            }}
          >

            <Typography
              variant="h6"
              gutterBottom
            >
              Security Policy Status
            </Typography>

            <Divider sx={{ mb: 3 }} />

            <Alert
              severity="success"
              icon={<CheckCircleIcon />}
            >
              Policy Engine Active —
              cryptographic enforcement is enabled.
            </Alert>

            <Grid
              container
              spacing={3}
              sx={{ mt: 1 }}
            >

              <Grid
                size={{
                  xs: 12,
                  md: 4,
                }}
              >

                <Typography
                  color="text.secondary"
                >
                  Policy Name
                </Typography>

                <Typography
                  variant="h6"
                  fontWeight="bold"
                  sx={{ mt: 0.5 }}
                >
                  {policy.policy_name ||
                    "Enterprise PQC Policy"}
                </Typography>

              </Grid>

              <Grid
                size={{
                  xs: 12,
                  md: 4,
                }}
              >

                <Typography
                  color="text.secondary"
                >
                  Security Level
                </Typography>

                <Typography
                  variant="h6"
                  fontWeight="bold"
                  sx={{ mt: 0.5 }}
                >
                  {policy.security_level ||
                    "HIGH"}
                </Typography>

              </Grid>

              <Grid
                size={{
                  xs: 12,
                  md: 4,
                }}
              >

                <Typography
                  color="text.secondary"
                >
                  Enforcement Status
                </Typography>

                <Box sx={{ mt: 0.5 }}>

                  <Chip
                    icon={<SecurityIcon />}
                    label={policyStatus}
                    color="success"
                  />

                </Box>

              </Grid>

            </Grid>

          </Paper>

        </Grid>

        {/* =====================================
            Approved Algorithms
            ===================================== */}

        <Grid
          size={{
            xs: 12,
            md: 6,
          }}
        >

          <Paper
            elevation={3}
            sx={{
              p: 3,
              minHeight: 280,
              borderRadius: 2,
            }}
          >

            <Typography
              variant="h6"
              gutterBottom
            >
              Approved Algorithms
            </Typography>

            <Typography
              color="text.secondary"
              sx={{ mb: 3 }}
            >
              Algorithms permitted by the enterprise
              cryptographic security policy.
            </Typography>

            {approvedAlgorithms.length === 0 ? (

              <Alert severity="info">
                No approved algorithms configured.
              </Alert>

            ) : (

              <Box>

                {approvedAlgorithms.map(
                  (algorithm) => (

                    <Chip
                      key={algorithm}
                      label={algorithm}
                      color="success"
                      icon={
                        <CheckCircleIcon />
                      }
                      sx={{
                        mr: 1,
                        mb: 1,
                      }}
                    />

                  )
                )}

              </Box>

            )}

          </Paper>

        </Grid>

        {/* =====================================
            Blocked Algorithms
            ===================================== */}

        <Grid
          size={{
            xs: 12,
            md: 6,
          }}
        >

          <Paper
            elevation={3}
            sx={{
              p: 3,
              minHeight: 280,
              borderRadius: 2,
            }}
          >

            <Typography
              variant="h6"
              gutterBottom
            >
              Blocked Algorithms
            </Typography>

            <Typography
              color="text.secondary"
              sx={{ mb: 3 }}
            >
              Algorithms prohibited because they do
              not meet enterprise security requirements.
            </Typography>

            {blockedAlgorithms.length === 0 ? (

              <Alert severity="success">
                No blocked algorithms configured.
              </Alert>

            ) : (

              <Box>

                {blockedAlgorithms.map(
                  (algorithm) => (

                    <Chip
                      key={algorithm}
                      label={algorithm}
                      color="error"
                      icon={
                        <BlockIcon />
                      }
                      sx={{
                        mr: 1,
                        mb: 1,
                      }}
                    />

                  )
                )}

              </Box>

            )}

          </Paper>

        </Grid>

        {/* =====================================
            Conditional Algorithms
            ===================================== */}

        {conditionalAlgorithms.length > 0 && (

          <Grid size={{ xs: 12 }}>

            <Paper
              elevation={3}
              sx={{
                p: 3,
                borderRadius: 2,
              }}
            >

              <Typography
                variant="h6"
                gutterBottom
              >
                Conditional Algorithms
              </Typography>

              <Typography
                color="text.secondary"
                sx={{ mb: 3 }}
              >
                Algorithms permitted only under
                defined security conditions or
                hybrid deployment.
              </Typography>

              <Box>

                {conditionalAlgorithms.map(
                  (algorithm) => (

                    <Chip
                      key={algorithm}
                      label={algorithm}
                      color="warning"
                      sx={{
                        mr: 1,
                        mb: 1,
                      }}
                    />

                  )
                )}

              </Box>

            </Paper>

          </Grid>

        )}

        {/* =====================================
            Quantum-Safe Policy Information
            ===================================== */}

        <Grid size={{ xs: 12 }}>

          <Paper
            elevation={3}
            sx={{
              p: 3,
              borderRadius: 2,
            }}
          >

            <Typography
              variant="h6"
              gutterBottom
            >
              Quantum-Safe Enforcement
            </Typography>

            <Divider sx={{ mb: 3 }} />

            <Grid
              container
              spacing={3}
            >

              <Grid
                size={{
                  xs: 12,
                  md: 4,
                }}
              >

                <Typography
                  color="text.secondary"
                >
                  PQC Key Encapsulation
                </Typography>

                <Typography
                  variant="h6"
                  fontWeight="bold"
                  sx={{ mt: 0.5 }}
                >
                  ML-KEM-768
                </Typography>

              </Grid>

              <Grid
                size={{
                  xs: 12,
                  md: 4,
                }}
              >

                <Typography
                  color="text.secondary"
                >
                  PQC Digital Signature
                </Typography>

                <Typography
                  variant="h6"
                  fontWeight="bold"
                  sx={{ mt: 0.5 }}
                >
                  ML-DSA-65
                </Typography>

              </Grid>

              <Grid
                size={{
                  xs: 12,
                  md: 4,
                }}
              >

                <Typography
                  color="text.secondary"
                >
                  Symmetric Encryption
                </Typography>

                <Typography
                  variant="h6"
                  fontWeight="bold"
                  sx={{ mt: 0.5 }}
                >
                  AES-256-GCM
                </Typography>

              </Grid>

            </Grid>

          </Paper>

        </Grid>

      </Grid>

    </Box>
  );
}

export default Policy;
