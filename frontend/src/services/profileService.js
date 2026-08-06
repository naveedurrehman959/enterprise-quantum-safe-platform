import api from "./api";


const getProfile = async () => {
    const response = await api.get("/profile");
    return response.data;
};


const updateProfile = async (data) => {
    const response = await api.put("/profile", data);
    return response.data;
};


const changePassword = async (data) => {
    const response = await api.put(
        "/profile/password",
        data
    );

    return response.data;
};


export default {
    getProfile,
    updateProfile,
    changePassword
};
