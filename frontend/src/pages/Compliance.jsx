import { useEffect, useState } from "react";

import {
  Grid,
  Paper,
  Typography,
  Chip,
} from "@mui/material";

import api from "../services/api";
import DashboardCard from "../components/DashboardCard";

function Compliance() {
  const [compliance, setCompliance] = useState(null);

  useEffect(() => {
    api
      .get("/compliance/status")
      .then((res) => {
        setCompliance(res.data);
      })
      .catch(console.error);
  }, []);

  if (!compliance) {
    return (
      <Typography>
        Loading Compliance...
      </Typography>
    );
  }

  return (
    <>
      <Typography
        variant="h4"
        sx={{ mb: 3 }}
      >
        Compliance Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Status"
            value={compliance.status}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Compliance Engine"
            value={compliance.compliance_engine}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Quantum Safe Ready"
            value={
              compliance.quantum_safe_ready
                ? "YES"
                : "NO"
            }
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Audit Ready"
            value={
              compliance.audit_ready
                ? "YES"
                : "NO"
            }
          />
        </Grid>

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
              Supported Frameworks
            </Typography>

            {compliance.frameworks_supported?.map(
              (framework) => (
                <Chip
                  key={framework}
                  label={framework}
                  color="primary"
                  sx={{
                    mr: 1,
                    mb: 1,
                  }}
                />
              )
            )}
          </Paper>
        </Grid>

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
              Integrations
            </Typography>

            <Typography>
              <strong>Policy Integration:</strong>{" "}
              {compliance.policy_integration}
            </Typography>

            <Typography sx={{ mt: 1 }}>
              <strong>Risk Engine Integration:</strong>{" "}
              {compliance.risk_engine_integration}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </>
  );
}

export default Compliance;
