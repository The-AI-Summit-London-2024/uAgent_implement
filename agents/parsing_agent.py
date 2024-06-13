from uagents import Agent, Context, Model
import gpt4_functions as gf

class AgentRequest(Model):
    file_path: str

class Response(Model):
    text: str

# Initialize agent
gpt4agent = Agent(
	name="gpt4agent",
	port=8002,
	seed="gpt4agent",
    endpoint="http://localhost:8002/submit",
)

# Introduce agent
@gpt4agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {gpt4agent.name}")
    ctx.logger.info(f"With address: {gpt4agent.address}")

# Run all required logic on startup
@gpt4agent.on_query(model=AgentRequest, replies={Response})
async def call_gpt4(ctx: Context, sender: str, _query: AgentRequest):
	
	ctx.logger.info(f"Received message from {sender}: {_query.file_path}")
	
	name = "Insurance Paralegal"
	assistant_desc = "You are an expert paralegal analyst. Use your knowledge base to answer questions about the provided pension insurance documents."

	client = gf.create_client()
	assistant = gf.create_assistant(client, name, assistant_desc, 'gpt-4o')
	prompt = """
	Summarize the provided document in 3 sentences, as if you would to an insurance attorney who is familiar with insurance related legal terms.
	Then provide 3 to 10 key bullet points that capture the most critical rules.
	Use only the latest provided document as your ground truth. Ignore all previous documents.
	"""

	filepaths = [f"agents/{_query.file_path}"]

	gf.upload_file(client, assistant, filepaths)	# comment this out after uploading file
	response, _ = gf.prompt_gpt4(client, assistant, prompt)

	ctx.logger.info(f"GTP4 Response: {response}")

	gf.clear_all_files(client)
    
	try:
		await ctx.send(sender, Response(text=str(response)))
	except Exception:
		await ctx.send(sender, Response(text="fail"))

if __name__ == "__main__":
	gpt4agent.run()