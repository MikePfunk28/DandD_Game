from security_measures import SecurityMeasures

class VPCDefender:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
        self.current_health = stats.max_health
        self.preparation_points = 100
        
        # Correctly initialize measures
        measures = SecurityMeasures()
        self.defensive_measures = measures.get_defensive_measures()
        self.offensive_measures = measures.get_offensive_measures()
        
        self.active_measures = []

    def add_active_measure(self, measure_name):
        for measure in self.defensive_measures:
            if measure.name.lower() == measure_name.lower():
                if self.preparation_points >= measure.cost:
                    self.preparation_points -= measure.cost
                    self.active_measures.append(measure)
                    return f"Implemented {measure.name}."
                else:
                    return "Insufficient preparation points."
        return "Measure not found."


    def is_alive(self):
        return self.current_health > 0

    def level_up(self):
        self.stats.level_up()
        self.current_health = self.stats.max_health