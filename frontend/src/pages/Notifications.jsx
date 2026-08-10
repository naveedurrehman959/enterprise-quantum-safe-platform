import { useEffect, useState } from "react";

import {
    Card,
    CardContent,
    Typography,
    Chip,
    Stack,
    Box,
    IconButton,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";

import notificationService from "../services/notificationService";

export default function Notifications() {
    const [notifications, setNotifications] =
        useState([]);

    const fetchNotifications = async () => {
        try {
            const data =
                await notificationService.getNotifications();

            setNotifications(
                data.notifications || []
            );
        } catch (error) {
            console.error(
                "Notification loading failed",
                error
            );
        }
    };

    useEffect(() => {
        let cancelled = false;

        const loadInitialNotifications = async () => {
            try {
                const data =
                    await notificationService.getNotifications();

                if (!cancelled) {
                    setNotifications(
                        data.notifications || []
                    );
                }
            } catch (error) {
                if (!cancelled) {
                    console.error(
                        "Notification loading failed",
                        error
                    );
                }
            }
        };

        loadInitialNotifications();

        return () => {
            cancelled = true;
        };
    }, []);

    return (
        <>
            <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                mb={3}
            >
                <Box>
                    <Typography variant="h4">
                        Security Notifications
                    </Typography>

                    <Typography
                        color="text.secondary"
                    >
                        Security events, migration alerts,
                        and platform activities
                    </Typography>
                </Box>

                <IconButton
                    color="primary"
                    onClick={fetchNotifications}
                    sx={{
                        border: "1px solid #d1d5db",
                        borderRadius: 2,
                    }}
                >
                    <RefreshIcon />
                </IconButton>
            </Box>

            <Chip
                label={`${notifications.length} Notifications`}
                color="primary"
                sx={{ mb: 3 }}
            />

            {notifications.length === 0 ? (
                <Typography color="text.secondary">
                    No security notifications available.
                </Typography>
            ) : (
                <Stack spacing={2}>
                    {notifications.map((notification) => (
                        <Card
                            key={notification.id}
                            elevation={3}
                        >
                            <CardContent>
                                <Typography variant="h6">
                                    {notification.title}
                                </Typography>

                                <Typography
                                    color="text.secondary"
                                    sx={{ mt: 1 }}
                                >
                                    {notification.message}
                                </Typography>

                                <Box sx={{ mt: 2 }}>
                                    <Chip
                                        label={
                                            notification.module
                                        }
                                        sx={{ mr: 1 }}
                                    />

                                    <Chip
                                        label={
                                            notification.status
                                        }
                                        color={
                                            notification.status ===
                                            "SUCCESS"
                                                ? "success"
                                                : notification.status ===
                                                  "WARNING"
                                                ? "warning"
                                                : "error"
                                        }
                                    />
                                </Box>

                                <Typography
                                    variant="body2"
                                    color="text.secondary"
                                    sx={{ mt: 2 }}
                                >
                                    {new Date(
                                        notification.timestamp
                                    ).toLocaleString()}
                                </Typography>
                            </CardContent>
                        </Card>
                    ))}
                </Stack>
            )}
        </>
    );
}
