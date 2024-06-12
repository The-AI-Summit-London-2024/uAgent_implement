from uagents import Agent, Bureau, Context,Model
from data_mapping_agent import mapping

class Message(Model):
    message: str
class Response(Model):
    text: str

AGENT_MAPPING_ADDRESS="agent1qfw0krjhp8dcrtee7kfy6xtrpmumrq4dj7vfmlx5zz4hjex872vkqsg02vc"

parsing = Agent(
    name="parsing",
    seed="documents parsing",
    port="8000",
    endpoint="http://localhost:8000/submit"
)

@parsing.on_event("startup")
async def get_address(ctx: Context):
    ctx.logger.info(f"doc parsing agent address: {ctx.agent.address}")

@parsing.on_interval(period=300.0)
async def send_message(ctx: Context):
    await ctx.send(AGENT_MAPPING_ADDRESS, Message(message="Hello there bob."))

@parsing.on_query(model=Message, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Message):
    ctx.logger.info("Query received")
    try:
        # do something here
        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))

if __name__ == "__main__":
    parsing.run()
