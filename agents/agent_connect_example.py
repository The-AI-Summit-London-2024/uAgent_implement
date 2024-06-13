from uagents import Agent, Context, Model

class TestRequest(Model):
    message: str

class Response(Model):
    text: str

agent = Agent(
    name="your_agent_name_here",
    seed="your_agent_seed_here",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {agent.name}")
    ctx.logger.info(f"With address: {agent.address}")
    ctx.logger.info(f"And wallet address: {agent.wallet.address()}")


@agent.on_query(model=TestRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info("Query received")
    try:
        # Prepare the response text to include the received query
        response_text = f"success - message received: {_query.message}"
        await ctx.send(sender, Response(text=response_text))
    except Exception as e:
        await ctx.send(sender, Response(text=f"fail - {str(e)}"))


if __name__ == "__main__":
    agent.run()