from uagents import Agent, Context, Model
import gpt4_functions as gf
import os

# TODO: Too much logging happening, figure out how to tune it down

import logging

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

class TestRequest(Model):
    message: str

class Response(Model):
    text: str

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
@gpt4agent.on_event("startup")
async def introduce_agent(ctx: Context):
	ctx.logger.error(f"Hello, I'm agent {gpt4agent.name} and my address is {gpt4agent.address}.")

# Run all required logic on startup
@gpt4agent.on_query(model=TestRequest, replies={Response})
async def call_gpt4(ctx: Context, sender: str, _query: TestRequest):

	name = "Insurance Paralegal"
	assistant_desc = "You are an expert paralegal analyst. Use your knowledge base to answer questions about the provided pension insurance documents."

	client, assistant = gf.create_assistant(name, assistant_desc, 'gpt-4o')
	prompt = """
	Summarize the provided document in 3 sentences, as if you would to an insurance attorney who is familiar with insurance related legal terms.
	Then provide 3 to 10 key bullet points that capture the most critical rules.
	Use only the latest provided document as your ground truth. Ignore all previous documents.
	"""

	filepaths = ["IBP_Problemstatement.docx"]

	# message_file = gf.upload_file(client, assistant, filepaths)	# comment this out after uploading file
	response, citations = gf.prompt_gpt4(client, assistant, prompt)

	print(response)
	print(citations)

	# Clean up files if needed
	# gf.clear_all_files(client)
	# gf.clear_all_vector_stores(client)

	# Store response in json
	ctx.storage.set("summary", response+"\n"+citations)
	
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