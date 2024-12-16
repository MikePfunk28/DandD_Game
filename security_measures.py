from security_common import SecurityStrategy

class SecurityMeasure:
    def __init__(self, name, description, cost, strategy, effectiveness=10):
        self.name = name
        self.description = description
        self.cost = cost
        self.strategy = strategy
        self.effectiveness = effectiveness

class SecurityMeasures:
    def __init__(self):
        self.measures = [
            # Defensive Measures
            SecurityMeasure(
                name="Firewall",
                description="Blocks unauthorized access",
                cost=10,
                strategy=SecurityStrategy.DEFENSIVE
            ),
            SecurityMeasure(
                name="Encryption",
                description="Secures data in transit",
                cost=15,
                strategy=SecurityStrategy.DEFENSIVE
            ),
            SecurityMeasure(
                name="DDoS Protection",
                description="Defends against DDoS attacks",
                cost=20,
                strategy=SecurityStrategy.DEFENSIVE
            ),
            # Offensive Measures
            SecurityMeasure(
                name="Penetration Test",
                description="Simulates attacks to uncover vulnerabilities",
                cost=18,
                strategy=SecurityStrategy.OFFENSIVE
            ),
            SecurityMeasure(
                name="Reconnaissance",
                description="Gathers information to test defenses",
                cost=12,
                strategy=SecurityStrategy.OFFENSIVE
            ),
            SecurityMeasure(
                name="Social Engineering Test",
                description="Evaluates human vulnerabilities through phishing simulations",
                cost=15,
                strategy=SecurityStrategy.OFFENSIVE
            ),
        ]

    def get_defensive_measures(self):
        return [measure for measure in self.measures if measure.strategy == SecurityStrategy.DEFENSIVE]

    def get_offensive_measures(self):
        return [measure for measure in self.measures if measure.strategy == SecurityStrategy.OFFENSIVE]
