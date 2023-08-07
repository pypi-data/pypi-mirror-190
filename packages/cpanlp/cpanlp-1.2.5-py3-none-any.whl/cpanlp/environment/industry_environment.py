from cpanlp.environment.economic_environment import *
class IndustryEnvironment(EconomicEnvironment):
    def __init__(self):
        super().__init__()
        self.add_factor("market_size", None)
        self.add_factor("market_growth", None)