import api from "./api";

const policyService = {

  /*
   * Get current enterprise policy
   */
  getStatus: () => {
    return api.get("/policy/status");
  },


  /*
   * Get all configurable policies
   */
  getPolicies: () => {
    return api.get("/policy/algorithms");
  },


  /*
   * Update policy for an algorithm
   *
   * Example:
   *
   * {
   *   enabled: true,
   *   deployment_mode: "HYBRID",
   *   enforcement_action: "ALLOW"
   * }
   */
  updatePolicy: (
    algorithmName,
    policy
  ) => {

    return api.put(
      `/policy/algorithm/${encodeURIComponent(
        algorithmName
      )}`,
      {
        enabled:
          policy.enabled,

        deployment_mode:
          policy.deployment_mode,

        enforcement_action:
          policy.enforcement_action
      }
    );
  },


  /*
   * Evaluate an algorithm against:
   *
   * Risk Assessment
   * +
   * Enterprise Policy
   */
  checkPolicy: (algorithm) => {

    return api.post(
      "/policy/check",
      {
        algorithm
      }
    );
  },


  /*
   * Risk-based policy evaluation
   */
  evaluateRisk: (algorithm) => {

    return api.post(
      "/policy/evaluate-risk",
      {
        algorithm
      }
    );
  }

};

export default policyService;
