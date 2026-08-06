import api from "./api";

const pkiService = {

  getCertificates() {
    return api.get("/pki/certificates");
  },

  issueCertificate(data) {
    return api.post("/pki/issue", data);
  },

  revokeCertificate(serial) {
    return api.post(`/pki/revoke/${serial}`);
  }

};

export default pkiService;
