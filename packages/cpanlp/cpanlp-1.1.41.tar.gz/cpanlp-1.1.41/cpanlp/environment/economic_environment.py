from cpanlp.environment.environment import *

class EconomicEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.add_factor("GDP", None)
        self.add_factor("unemployment_rate", None)
    
    def set_gdp(self, gdp):
        self.factors["GDP"] = gdp
    
    def set_unemployment_rate(self, unemployment_rate):
        self.factors["unemployment_rate"] = unemployment_rate