from uagents import Agent, Context, Model
import gpt4_functions as gf

class Message(Model):
	message: str

# Initialize agent
gpt4agent = Agent(
	name="answersagent",
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
	
    name = "Insurance Paralegal"
    assistant_desc = "You are an expert paralegal analyst. Use your knowledge base to answer questions about the provided pension insurance documents."
	
    client = gf.create_client()
    assistant = gf.create_assistant(client, name, assistant_desc, 'gpt-4o')

    # # TODO: Take in individual member's information as input (json format)
    indiv_input ="""
        {
            "member_id": 2752,
            "name": "John Doe",
            "dob": "1990-01-01",
            "company_join_date": "2010-01-01",
            "gender": "F",
            "date_of_leaving": None,
            "date_of_retirement": None,
            "date_of_death": None,
            "marital_status": "married",
            "marriage_date": "2016-01-01",
            "spouse_dob": "1990-01-01",
            "children": 2,
            "children_dob": ["2010-01-01", "2012-01-01"],
        }
    """

    questions = [
        {
            "question": "What is the frequency and mode of pension payment for the member?",
            "relevant_sections": [
                "Section 1.1 (Frequency Of Payment)",
                "Section 1.2 (In Advance or in Arrears)"
            ]
        },
        {
            "question": "What is the normal retirement date (NRD) for the member?",
            "relevant_sections": [
                "Section 2.1.1 (Normal Retirement Date)"
            ]
        },
        {
            "question": "Is early retirement available for the member and are there any conditions?",
            "relevant_sections": [
                "Section 2.2 (Early Retirement)",
                "Section 2.2.1 (Early Retirement Eligibility)",
                "Section 2.2.2 (Early Retirement Ill Health Eligibility)"
            ]
        },
        {
            "question": "What are the commutation options available to the member?",
            "relevant_sections": [
                "Section 2.4 (Commutation Available)"
            ]
        },
        {
            "question": "What happens to the pension on the death of the member before normal retirement date?",
            "relevant_sections": [
                "Section 5.1 (Widow/Widower’s Pension)",
                "Section 5.2 (Lump Sum)",
                "Section 5.3 (Children’s Pension)",
                "Section 5.4 (Start date of Widow/Widower’s pension)"
            ]
        },
        {
            "question": "What benefits are provided if the member dies after taking retirement benefits?",
            "relevant_sections": [
                "Section 6.1 (Qualifying Spouse’s Pension)",
                "Section 6.2 (Lump Sum)",
                "Section 6.3 (Qualifying Children’s Pension)"
            ]
        },
        {
            "question": "What benefits are provided if the member dies after reaching normal retirement date without taking retirement benefits?",
            "relevant_sections": [
                "Section 7.1 (Qualifying Spouse’s Pension)",
                "Section 7.2 (Lump Sum)",
                "Section 7.3 (Qualifying Children’s Pension)"
            ]
        },
        {
            "question": "Who qualifies as a dependant under the scheme's definitions?",
            "relevant_sections": [
                "Section 8.1 (Qualifying Spouse)",
                "Section 8.2 (Qualifying Child)"
            ]
        },
        {
            "question": "What are the pension revaluation rates during deferment?",
            "relevant_sections": [
                "Section 3.1 (Revaluation Rates)"
            ]
        },
        {
            "question": "What are the pension increase rates in payment?",
            "relevant_sections": [
                "Section 4.1 (Pension Increase Rates in Payment)"
            ]
        }
    ]

    selected_qsn_idx = 4
    question = questions[selected_qsn_idx]['question']
    relevant_sections = questions[selected_qsn_idx]['relevant_sections']

    indiv_info = indiv_input
    prompt = ""
    if indiv_info:
        prompt += f"Given the following individual's information: {indiv_info}, "

    prompt += f"based on {', '.join(relevant_sections)} in the document, {question}"
    print(prompt)

    response, citations = gf.prompt_gpt4(client, assistant, prompt)

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