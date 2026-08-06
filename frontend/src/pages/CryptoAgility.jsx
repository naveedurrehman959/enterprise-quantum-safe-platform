import { useEffect, useState } from "react";

import {
  Grid,
  Paper,
  Typography,
  Chip,
} from "@mui/material";

import api from "../services/api";
import DashboardCard from "../components/DashboardCard";

function CryptoAgility() {
  const [crypto, setCrypto] = useState(null);

  useEffect(() => {
    api
      .get("/crypto-agility/status")
      .then((res) => {
        setCrypto(res.data);
      })
      .catch(console.error);
  }, []);

  if (!crypto) {
    return <Typography>Loading Crypto Agility...</Typography>;
  }

  return (
    <>
      <Typography
        variant="h4"
        sx={{ mb: 3 }}
      >
        Crypto Agility Engine
      </Typography>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Engine Status"
            value={crypto.status}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Hybrid Cryptography"
            value={crypto.hybrid_crypto}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Algorithm Switching"
            value={crypto.algorithm_switching}
          />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <DashboardCard
            title="Migration Engine"
            value={crypto.migration_engine}
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
              Supported Post-Quantum Algorithms
            </Typography>

            {crypto.supported_pqc?.map((algorithm) => (
              <Chip
                key={algorithm}
                label={algorithm}
                color="primary"
                sx={{ mr: 1, mb: 1 }}
              />
            ))}
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
              Architecture Status
            </Typography>

            <Typography>
              Crypto Agility Framework is active and ready
              for enterprise quantum-safe migration.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </>
  );
}

export default CryptoAgility;
