import api from "./api";


const vaultService = {

    getStatus(){
        return api.get("/vault/status");
    },


    listSecrets(){
        return api.get("/vault/list-secrets");
    },


    storeSecret(data){
        return api.post(
            "/vault/store-secret",
            data
        );
    },


    deleteSecret(name){
        return api.delete(
            `/vault/delete-secret/${name}`
        );
    }

};


export default vaultService;
