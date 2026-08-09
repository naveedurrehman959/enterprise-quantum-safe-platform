import api from "./api";

const assetDiscoveryService = {

  getAssets: async () => {
    const response = await api.get("/discovery");
    return response.data;
  },

  scanAsset: async (target, port = 443) => {
    const response = await api.post("/discovery/scan", {
      target,
      port: Number(port),
    });

    return response.data;
  },

  rescanAsset: async (id) => {
    const response = await api.post(
      `/discovery/${id}/rescan`
    );

    return response.data;
  },

  deleteAsset: async (id) => {
    const response = await api.delete(
      `/discovery/${id}`
    );

    return response.data;
  },

};

export default assetDiscoveryService;
