import { useEffect, useState } from "react";

import {
    Paper,
    Typography,
    Chip,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Box,
} from "@mui/material";

import { DataGrid } from "@mui/x-data-grid";

import api from "../services/api";
import migrationService from "../services/migrationService";

function Inventory() {
    const [rows, setRows] = useState([]);
    const [migrationPlan, setMigrationPlan] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let cancelled = false;

        const fetchInventory = async () => {
            try {
                const response =
                    await api.get("/inventory/algorithms");

                const algorithms =
                    response.data.algorithms || [];

                const formatted = algorithms.map((item) => ({
                    id: item.id,
                    asset_name: item.algorithm_name,
                    algorithm_name: item.algorithm_name,
                    algorithm_type:
                        item.category || "UNKNOWN",
                    quantum_risk:
                        item.risk_level || "UNKNOWN",
                    migration_status:
                        item.deployment_mode || "UNKNOWN",
                    description: item.description,
                }));

                if (!cancelled) {
                    setRows(formatted);
                }
            } catch (error) {
                if (!cancelled) {
                    console.error(
                        "Inventory loading failed",
                        error
                    );
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        };

        fetchInventory();

        return () => {
            cancelled = true;
        };
    }, []);

    const generateMigrationPlan = async (algorithm) => {
        try {
            const response =
                await migrationService.createPlan(
                    algorithm
                );

            setMigrationPlan(response.data);
        } catch (error) {
            console.error(
                "Migration plan failed",
                error
            );
        }
    };

    const columns = [
        {
            field: "asset_name",
            headerName: "Asset",
            flex: 1,
        },

        {
            field: "algorithm_name",
            headerName: "Algorithm",
            flex: 1,
        },

        {
            field: "algorithm_type",
            headerName: "Type",
            flex: 1,

            renderCell: (params) => (
                <Chip
                    label={
                        params.value || "UNKNOWN"
                    }
                    color={
                        params.value?.includes("PQC")
                            ? "success"
                            : "warning"
                    }
                    size="small"
                />
            ),
        },

        {
            field: "quantum_risk",
            headerName: "Quantum Risk",
            width: 150,

            renderCell: (params) => (
                <Chip
                    label={
                        params.value || "UNKNOWN"
                    }
                    color={
                        params.value === "SAFE"
                            ? "success"
                            : params.value === "CRITICAL"
                            ? "error"
                            : params.value === "HIGH"
                            ? "warning"
                            : "default"
                    }
                    size="small"
                />
            ),
        },

        {
            field: "migration_status",
            headerName: "Migration",
            width: 150,
        },

        {
            field: "action",
            headerName: "Action",
            width: 150,
            sortable: false,

            renderCell: (params) => (
                <Button
                    size="small"
                    variant="contained"
                    onClick={() =>
                        generateMigrationPlan(
                            params.row.algorithm_name
                        )
                    }
                >
                    Migrate
                </Button>
            ),
        },
    ];

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

    return (
        <>
            <Typography
                variant="h4"
                sx={{ mb: 3 }}
            >
                Cryptographic Algorithm Inventory
            </Typography>

            <Paper
                sx={{
                    height: 550,
                    p: 2,
                }}
            >
                <DataGrid
                    rows={rows}
                    columns={columns}
                    pageSizeOptions={[5, 10]}
                    disableRowSelectionOnClick
                />
            </Paper>

            {migrationPlan && (
                <Card
                    sx={{ mt: 3 }}
                    elevation={3}
                >
                    <CardContent>
                        <Typography variant="h6">
                            Migration Plan Generated
                        </Typography>

                        <pre>
                            {JSON.stringify(
                                migrationPlan,
                                null,
                                2
                            )}
                        </pre>
                    </CardContent>
                </Card>
            )}
        </>
    );
}

export default Inventory;
