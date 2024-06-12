from collections import OrderedDict
from uagents import Agent, Bureau, Context
from models.client_info import ClientInfo
from client_info_receive import info_reciever_agent
from config import CLIENT_INFO_RECEIVER_AGENT

QUESTIONS = OrderedDict([
    ("name", "Name: "),
    ("dob", "Date of birth: "),
    ("company_join_date", "Company join date: "),
    ("gender", "Gender: "),
    ("date_of_leaving", "Date of leaving: "),
    ("date_of_retirement", "Date of retirement: "),
    ("date_of_death", "Date of death: "),
    ("marital_status", "Marital status: "),
    ("children", "Children: "),
    ("dependants", "Dependants: "),
    ("spouse_dob", "Spouse date of birth: ")
    ]
)

client_agent = Agent(name="client_agent", seed="client info recovery phrase")

@client_agent.on_event("startup")
async def send_client_info(ctx: Context):
    client_info = gain_user_info()
    await ctx.send(CLIENT_INFO_RECEIVER_AGENT, client_info)

def gain_user_info():
    client_info = ClientInfo()
    for key, value in QUESTIONS.items():
        setattr(client_info, key, input(value))
    return client_info

bureau = Bureau()
bureau.add(client_agent)
bureau.add(info_reciever_agent)

if __name__ == "__main__":
    bureau.run()