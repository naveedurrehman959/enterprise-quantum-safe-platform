import api from "./api";

export async function getDashboard() {
    const response = await api.get("/monitoring/dashboard");
    return response.data;
}

export async function getSystemHealth() {
    const response = await api.get("/monitoring/system-health");
    return response.data;
}
