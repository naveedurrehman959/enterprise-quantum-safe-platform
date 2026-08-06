import {
  Box,
  Typography,
  LinearProgress,
} from "@mui/material";

function MigrationProgress({ safe, vulnerable }) {

  const total = safe + vulnerable;

  const progress =
    total === 0
      ? 0
      : Math.round((safe / total) * 100);

  return (
    <Box>

      <Typography
        variant="h6"
        gutterBottom
      >
        Migration Progress
      </Typography>

      <LinearProgress
        variant="determinate"
        value={progress}
        sx={{
          height: 12,
          borderRadius: 5,
          mb: 2,
        }}
      />

      <Typography>
        Progress: {progress}%
      </Typography>

      <Typography>
        Safe Assets: {safe}
      </Typography>

      <Typography>
        Vulnerable Assets: {vulnerable}
      </Typography>

      <Typography>
        Total Assets: {total}
      </Typography>

    </Box>
  );
}

export default MigrationProgress;
