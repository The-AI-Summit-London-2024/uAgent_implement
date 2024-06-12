from uagents import Agent, Bureau, Context, Model

class Response(Model):
    text: str
class Message(Model):
    message: str

mapping = Agent(
    name="mapping",
    seed="data mapping",
)

@mapping.on_event("startup")
async def get_pdf(ctx: Context):
    ctx.logger.info(f"mapping address mapping: {ctx.agent.address}")

@mapping.on_message(model=Message)
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    response_message = f"Processed the message: {msg.message}"
    #await ctx.send(sender, Message(message=response_message))

@mapping.on_query(model=Message, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: Message):
    ctx.logger.info("Query received")
    try:
        # do something here
        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))