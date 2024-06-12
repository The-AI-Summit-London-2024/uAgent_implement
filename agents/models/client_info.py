from uagents import Model

class ClientInfo(Model):
    name: str = None               # "John Doe"
    dob: str = None                # "1990-01-01",
    company_join_date: str = None  # "2010-01-01",
    gender: str = None             # "F",
    date_of_leaving: str = None    # "2020-01-01",
    date_of_retirement: str = None # "2020-01-01",
    date_of_death: str = None      # "2020-01-01",
    marital_status: str = None     # "married",
    children: int = None           # 2,
    dependants: int = None         # 1,
    spouse_dob: str = None         # "1990-01-01",