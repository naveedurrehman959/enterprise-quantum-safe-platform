import { useEffect, useState } from "react";

import {
    Card,
    CardContent,
    Typography,
    Button,
    TextField,
    Stack,
    Chip,
} from "@mui/material";

import vaultService from "../services/vaultService";

function Vault() {
    const [status, setStatus] = useState(null);
    const [secrets, setSecrets] = useState([]);

    const [secret, setSecret] = useState({
        secret_name: "",
        secret_value: "",
        secret_type: "KEY",
    });

    const loadVault = async () => {
        try {
            const statusResponse =
                await vaultService.getStatus();

            setStatus(statusResponse.data);

            const secretsResponse =
                await vaultService.listSecrets();

            setSecrets(
                secretsResponse.data.secrets || []
            );
        } catch (error) {
            console.error(
                "Vault loading failed",
                error
            );
        }
    };

    useEffect(() => {
        let cancelled = false;

        const loadInitialVault = async () => {
            try {
                const statusResponse =
                    await vaultService.getStatus();

                const secretsResponse =
                    await vaultService.listSecrets();

                if (!cancelled) {
                    setStatus(statusResponse.data);

                    setSecrets(
                        secretsResponse.data.secrets || []
                    );
                }
            } catch (error) {
                if (!cancelled) {
                    console.error(
                        "Vault loading failed",
                        error
                    );
                }
            }
        };

        loadInitialVault();

        return () => {
            cancelled = true;
        };
    }, []);

    const store = async () => {
        try {
            await vaultService.storeSecret(secret);

            setSecret({
                secret_name: "",
                secret_value: "",
                secret_type: "KEY",
            });

            await loadVault();
        } catch (error) {
            console.error(
                "Secret storage failed",
                error
            );
        }
    };

    return (
        <>
            <Typography
                variant="h4"
                sx={{ mb: 3 }}
            >
                Enterprise Vault
            </Typography>

            {status && (
                <Card
                    elevation={3}
                    sx={{ mb: 3 }}
                >
                    <CardContent>
                        <Stack
                            direction="row"
                            spacing={2}
                            alignItems="center"
                        >
                            <Typography>
                                Vault Status
                            </Typography>

                            <Chip
                                label={
                                    status.status ||
                                    status.health ||
                                    "Available"
                                }
                                color="success"
                            />
                        </Stack>
                    </CardContent>
                </Card>
            )}

            <Card elevation={3}>
                <CardContent>
                    <Typography
                        variant="h6"
                        sx={{ mb: 3 }}
                    >
                        Store Secret
                    </Typography>

                    <Stack spacing={2}>
                        <TextField
                            label="Secret Name"
                            value={secret.secret_name}
                            onChange={(event) =>
                                setSecret({
                                    ...secret,
                                    secret_name:
                                        event.target.value,
                                })
                            }
                            fullWidth
                        />

                        <TextField
                            label="Secret Value"
                            type="password"
                            value={secret.secret_value}
                            onChange={(event) =>
                                setSecret({
                                    ...secret,
                                    secret_value:
                                        event.target.value,
                                })
                            }
                            fullWidth
                        />

                        <Button
                            variant="contained"
                            onClick={store}
                        >
                            Store Secret
                        </Button>
                    </Stack>
                </CardContent>
            </Card>

            <Card
                elevation={3}
                sx={{ mt: 3 }}
            >
                <CardContent>
                    <Typography
                        variant="h6"
                        sx={{ mb: 2 }}
                    >
                        Stored Secrets
                    </Typography>

                    {secrets.length === 0 ? (
                        <Typography
                            color="text.secondary"
                        >
                            No secrets found.
                        </Typography>
                    ) : (
                        <Stack spacing={1}>
                            {secrets.map((item) => (
                                <Card
                                    key={
                                        item.id ||
                                        item.secret_name
                                    }
                                    variant="outlined"
                                >
                                    <CardContent>
                                        <Typography>
                                            {item.secret_name ||
                                                item.name ||
                                                "Unnamed Secret"}
                                        </Typography>

                                        <Chip
                                            label={
                                                item.secret_type ||
                                                "KEY"
                                            }
                                            size="small"
                                            sx={{ mt: 1 }}
                                        />
                                    </CardContent>
                                </Card>
                            ))}
                        </Stack>
                    )}
                </CardContent>
            </Card>
        </>
    );
}

export default Vault;
