class RiskTags(object):
    FLIGHT_RISK = "FLIGHT_RISK"
    HIGH_IMPACT_EMPLOYEE = "HIGH_IMPACT_EMPLOYEE"
    ELEVATED_ACCESS_PRIVILEGES = "ELEVATED_ACCESS_PRIVILEGES"
    PERFORMANCE_CONCERNS = "PERFORMANCE_CONCERNS"
    SUSPICIOUS_SYSTEM_ACTIVITY = "SUSPICIOUS_SYSTEM_ACTIVITY"
    POOR_SECURITY_PRACTICES = "POOR_SECURITY_PRACTICES"
    CONTRACT_EMPLOYEE = "CONTRACT_EMPLOYEE"

    def __iter__(self):
        return iter(
            [
                self.FLIGHT_RISK,
                self.HIGH_IMPACT_EMPLOYEE,
                self.ELEVATED_ACCESS_PRIVILEGES,
                self.PERFORMANCE_CONCERNS,
                self.SUSPICIOUS_SYSTEM_ACTIVITY,
                self.POOR_SECURITY_PRACTICES,
                self.CONTRACT_EMPLOYEE,
            ]
        )