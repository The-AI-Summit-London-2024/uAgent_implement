from uagents import Agent, Bureau, Context,Model
from data_mapping_agent import mapping

class Message(Model):
    message: str


AGENT_MAPPING_ADDRESS="agent1qfw0krjhp8dcrtee7kfy6xtrpmumrq4dj7vfmlx5zz4hjex872vkqsg02vc"

parsing = Agent(
    name="parsing",
    seed="documents parsing",
)
 
@parsing.on_interval(period=300.0)
async def send_message(ctx: Context):
    await ctx.send(AGENT_MAPPING_ADDRESS, Message(message="Hello there bob."))

bureau = Bureau(port=8001)
bureau.add(parsing)
bureau.add(mapping)


if __name__ == "__main__":
    bureau.run()
