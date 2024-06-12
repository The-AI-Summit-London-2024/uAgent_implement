from uagents import Agent, Context, Model
import gpt4_functions as gf

class Message(Model):
	message: str

# Initialize agent
gpt4agent = Agent(
	name="gpt4agent",
	port=8001,
	seed="gpt4agent secret phrase",
	endpoint=["http://127.0.0.1:8001/submit"],
)

# Introduce agent
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {gpt4agent.name} and my address is {gpt4agent.address}.")

# Run all required logic on startup
@gpt4agent.on_event("startup")
async def initialize_gpt4(ctx: Context):
	
    name = "Insurance Paralegal"
    assistant_desc = "You are an expert paralegal analyst. Use your knowledge base to answer questions about the provided pension insurance documents."
	
    client, assistant = gf.create_assistant(name, assistant_desc, 'gpt-4o')
    prompt = "Summarize the document in 3 sentences"

    response, citations = gf.upload_file_prompt(client, assistant, prompt)

    print(response)
    print(citations)
	
# Send delta calories to grocery agent

# RECIPIENT_ADDRESS = (
# 	"groceryagent://agent1qt27mhu8js84x7zh30sxegf0m5va2gxtk3sqns4ptvrutzv8l0kuke9qq43"
# )

# @gpt4agent.on_interval(period=60.0)
# async def send_message(ctx: Context):
# 	# ctx.logger.info(f"Sending message to {RECIPIENT_ADDRESS}")
# 	# await ctx.send(RECIPIENT_ADDRESS, Message(message="Hello there testagent."))
	
# 	delta = ctx.storage.get("delta")
# 	await ctx.send(RECIPIENT_ADDRESS, Message(message=str(delta)))

if __name__ == "__main__":
	gpt4agent.run()