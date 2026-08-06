import api from "./api";

const policyService = {

    getStatus: () => {
        return api.get("/policy/status");
    }

};

export default policyService;
