import api from "./api";

const getNotifications = async () => {
  const res = await api.get("/notifications/");
  return res.data;
};

export default {
  getNotifications,
};
