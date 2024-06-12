from uagents import Agent, Context
from models.client_info import ClientInfo

info_reciever_agent = Agent(name="info_reciever", seed="info_reciever recovery phrase")

@info_reciever_agent.on_message(model=ClientInfo)
async def info_reciever_message_handler(ctx: Context, sender: str, msg: ClientInfo):
    ctx.logger.info(f"Received {msg}")
