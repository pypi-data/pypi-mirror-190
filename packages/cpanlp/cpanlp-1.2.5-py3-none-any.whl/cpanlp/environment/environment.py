class Environment:
    def __init__(self):
        self.factors = {}
    
    def add_factor(self, factor, value):
        self.factors[factor] = value
    
    def get_factor(self, factor):
        return self.factors.get(factor, None)