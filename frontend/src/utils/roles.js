export const ROLE_PERMISSIONS = {
    admin: [
        "*"
    ],

    analyst: [
        "/dashboard",
        "/analytics",
        "/discovery",
        "/risk",
        "/monitoring",
        "/reports",
        "/search"
    ],

    compliance: [
        "/dashboard",
        "/compliance",
        "/audit",
        "/reports"
    ],

    pki: [
        "/dashboard",
        "/discovery",
        "/pki",
        "/crypto-agility",
        "/inventory"
    ],

    user: [
        "/dashboard",
        "/profile"
    ]
};
