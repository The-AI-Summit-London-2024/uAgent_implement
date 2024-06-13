from uagents import Agent, Context, Model
import gpt4_functions as gf

class Message(Model):
	message: str

class AgentRequest(Model):
    file_path: str

class Response(Model):
    text: str

# Initialize agent
qna_agent = Agent(
	name="questionsagent",
	port=8001,
	seed="qna_agent secret phrase",
	endpoint=["http://127.0.0.1:8001/submit"],
)

# Introduce agent
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {qna_agent.name} and my address is {qna_agent.address}.")

@qna_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"With address: {qna_agent.address}")


# Run all required logic on startup
@qna_agent.on_query(model=AgentRequest, replies={Response})
async def call_gpt4(ctx: Context, sender: str, _query: AgentRequest):
	
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
    filepaths = [f"agents/{_query.file_path}"]
    gf.upload_file(client, assistant, filepaths)
    response, _ = gf.prompt_gpt4(client, assistant, prompt)
    print(response)

    try:
        await ctx.send(sender, Response(text=str(response)))
    except Exception:
        await ctx.send(sender, Response(text="fail"))


if __name__ == "__main__":
	qna_agent.run()