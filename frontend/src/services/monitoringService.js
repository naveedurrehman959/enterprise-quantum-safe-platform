import api from "./api";

const monitoringService = {

  getDashboard() {
    return api.get("/monitoring/dashboard");
  },

  getSystemHealth() {
    return api.get("/monitoring/system-health");
  },
  getServices() {
    return api.get("/monitoring/services");
  },
  getCryptoMetrics() {
    return api.get("/monitoring/crypto-metrics");
  },

  getPlatformStatus() {
    return api.get("/monitoring/platform-status");
  },

  getQuantumReadiness() {
    return api.get("/monitoring/quantum-readiness");
  },

  getPKIStatus() {
    return api.get("/monitoring/pki-status");
  },

  getVaultStatus() {
    return api.get("/monitoring/vault-status");
  }

};

export default monitoringService;
