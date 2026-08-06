import { useEffect, useState } from "react";

import {
  Grid,
  Paper,
  Typography,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";

import DashboardCard from "../components/DashboardCard";

import api from "../services/api";
import migrationService from "../services/migrationService";

function Risk() {
  const [risk, setRisk] = useState(null);
  const [algorithm, setAlgorithm] = useState("RSA-2048");
  const [plan, setPlan] = useState(null);

  useEffect(() => {
    api
      .get("/risk/assessment")
      .then((res) => setRisk(res.data))
      .catch(console.error);
  }, []);

  const generateMigrationPlan = async () => {
    try {
      const response =
        await migrationService.createPlan(
          algorithm
        );

      setPlan(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  if (!risk) {
    return (
      <Typography>
        Loading Risk Assessment...
      </Typography>
    );
  }

  return (
    <>
      <Typography
        variant="h4"
        sx={{ mb: 3 }}
      >
        Risk Assessment
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
          <DashboardCard
            title="Total Assets"
            value={risk.total_assets}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
          <DashboardCard
            title="Safe Assets"
            value={risk.safe_assets}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
          <DashboardCard
            title="Medium Risk"
            value={risk.medium_risk}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
          <DashboardCard
            title="High Risk"
            value={risk.high_risk}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
          <DashboardCard
            title="Critical Risk"
            value={risk.critical_risk}
          />
        </Grid>

        <Grid size={{ xs: 12 }}>
          <Paper
            elevation={3}
            sx={{
              mt: 2,
              p: 3,
              borderRadius: 2,
            }}
          >
            <Typography
              variant="h6"
              gutterBottom
            >
              Quantum Migration Recommendation
            </Typography>

            <FormControl
              sx={{ minWidth: 220 }}
            >
              <InputLabel>
                Algorithm
              </InputLabel>

              <Select
                value={algorithm}
                label="Algorithm"
                onChange={(e) =>
                  setAlgorithm(e.target.value)
                }
              >
                <MenuItem value="RSA-2048">
                  RSA-2048
                </MenuItem>

                <MenuItem value="ECC">
                  ECC
                </MenuItem>

                <MenuItem value="ECDSA">
                  ECDSA
                </MenuItem>
              </Select>
            </FormControl>

            <Button
              variant="contained"
              sx={{ ml: 2 }}
              onClick={generateMigrationPlan}
            >
              Generate Migration Plan
            </Button>
          </Paper>
        </Grid>

        {plan && (
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
                Migration Plan
              </Typography>

              <pre>
                {JSON.stringify(
                  plan,
                  null,
                  2
                )}
              </pre>
            </Paper>
          </Grid>
        )}
      </Grid>
    </>
  );
}

export default Risk;
