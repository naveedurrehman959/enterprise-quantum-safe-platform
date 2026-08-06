import api from "./api";


const migrationService = {

    getStatus: () => {
        return api.get("/migration/status");
    },


    getReport: () => {
        return api.get("/migration/report");
    },


    analyze: (algorithm) => {
        return api.post(
            "/migration/analyze",
            {
                algorithm: algorithm
            }
        );
    },


    createPlan: (algorithm) => {
        return api.post(
            "/migration/plan",
            {
                algorithm: algorithm
            }
        );
    }

};


export default migrationService;
