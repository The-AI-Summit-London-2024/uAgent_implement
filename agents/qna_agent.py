from uagents import Agent, Context, Model
import gpt4_functions as gf

class Message(Model):
	message: str

# Initialize agent
gpt4agent = Agent(
	name="questionsagent",
	port=8001,
	seed="gpt4agent secret phrase",
	endpoint=["http://127.0.0.1:8001/submit"],
)

# Introduce agent
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {gpt4agent.name} and my address is {gpt4agent.address}.")

# Run all required logic on startup
@gpt4agent.on_event("startup")
async def call_gpt4(ctx: Context):
    ctx.logger.info(f"Starting up {gpt4agent.name}")
    ctx.logger.info(f"With address: {gpt4agent.address}")
    ctx.logger.info(f"And wallet address: {gpt4agent.wallet.address()}")

    name = "Insurance Paralegal"
    assistant_desc = "You are an expert paralegal analyst. Use your knowledge base to answer questions about the provided pension insurance documents."
	
    client = gf.create_client()
    assistant = gf.create_assistant(client, name, assistant_desc, 'gpt-4o')

    json_output_format = """
     {"question": "What is the frequency and mode of pension payment for the member?", "relevant_sections": ["Section 1.1 (Frequency Of Payment)",
      "Section 1.2 (In Advance or in Arrears)"]}
    """
    prompt = f"Generate a json string of 10 questions that can be answered based on the policy document, given an individual member's information. \
    Indicate which sections in the document are relevant to each question, in json format. For example: {json_output_format}"

    print(prompt)
    filepaths = ["agents/IBP_Problemstatement.docx"]
    message_file = gf.upload_file(client, assistant, filepaths)
    response, citations = gf.prompt_gpt4(client, assistant, prompt)
    print(response)
    # print(citations)


if __name__ == "__main__":
	gpt4agent.run()