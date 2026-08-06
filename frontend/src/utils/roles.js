export const ROLE_PERMISSIONS = {

    admin: [
        "*"
    ],

    analyst: [
        "/dashboard",
        "/analytics",
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
        "/pki",
        "/crypto-agility",
        "/inventory"
    ],

    user: [
        "/dashboard",
        "/profile"
    ]

};
