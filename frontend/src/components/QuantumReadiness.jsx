import {
    Card,
    CardContent,
    Typography,
    LinearProgress,
    Stack,
    Chip
} from "@mui/material";

export default function QuantumReadiness({

    score=0,
    safeAssets=0,
    vulnerableAssets=0

}){

    return(

        <Card
            elevation={3}
            sx={{height:"100%"}}
        >

            <CardContent>

                <Typography
                    variant="h6"
                    gutterBottom
                >
                    Quantum Readiness
                </Typography>

                <LinearProgress
                    variant="determinate"
                    value={score}
                    sx={{
                        height:12,
                        borderRadius:5,
                        mt:3
                    }}
                />

                <Typography
                    variant="h4"
                    mt={2}
                    fontWeight="bold"
                >
                    {score}%
                </Typography>

                <Stack
                    direction="row"
                    spacing={1}
                    mt={3}
                >

                    <Chip
                        color="success"
                        label={`Safe ${safeAssets}`}
                    />

                    <Chip
                        color="error"
                        label={`Risk ${vulnerableAssets}`}
                    />

                </Stack>

            </CardContent>

        </Card>

    );

}
