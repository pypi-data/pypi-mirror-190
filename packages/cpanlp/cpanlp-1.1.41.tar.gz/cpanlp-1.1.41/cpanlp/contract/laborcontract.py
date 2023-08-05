from cpanlp.contract.contract import *
class LaborContract(Contract):
    accounts = []
    def __init__(self, parties, consideration,obligations,salary):
        super().__init__(parties,obligations, purpose, terms,contract_number,clauses,enforceability,legality,consideration,offer,acceptance,start_date,end_date,transaction_cost,is_active,hidden_terms,is_complete)
        self.employee = None
        self.employer = None
        self.salary = salary
        LaborContract.accounts.append(self)