import api from "./api";

const reportService = {

  getReport: () =>
    api.get("/reports"),

  getSummary: () =>
    api.get("/reports/summary"),

  getRiskReport: () =>
    api.get("/reports/risk"),

  getComplianceReport: () =>
    api.get("/reports/compliance"),

  getMigrationReport: () =>
    api.get("/reports/migration"),

  getAuditReport: () =>
    api.get("/reports/audit"),

  getCertificateReport: () =>
    api.get("/reports/certificates"),

  exportPDF: () =>
    api.get("/reports/export/pdf", {
      responseType: "blob",
    }),

  exportCSV: () =>
    api.get("/reports/export/csv", {
      responseType: "blob",
    }),

};

export default reportService;
