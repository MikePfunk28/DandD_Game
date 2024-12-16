from security_common import SecurityStrategy

class SecurityMeasure:
    def __init__(self, name, description, cost, strategy):
        self.name = name
        self.description = description
        self.cost = cost
        self.strategy = strategy
        
    @staticmethod
    def get_defensive_measures():
        return [
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
        ]

    @staticmethod
    def get_offensive_measures():
        return [
            SecurityMeasure(
                name="Intrusion Detection", 
                description="Identifies suspicious activity", 
                cost=12, 
                strategy=SecurityStrategy.OFFENSIVE
            ),
            SecurityMeasure(
                name="Penetration Test", 
                description="Simulates attacks for testing", 
                cost=18, 
                strategy=SecurityStrategy.OFFENSIVE
            ),
        ]
