import api from "./api";

const settingsService = {

  getSettings() {
    return api.get("/settings");
  },

  updateSettings(data) {
    return api.put("/settings", data);
  },

};

export default settingsService;
