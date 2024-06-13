# uAgent_implement


## Description
Insurance companies frequently need to modify and customize pricing schemes (PRTs) for different clients to match their needs.
This takes considerable effort across multiple internal teams: legal, compliance, actuary, claims management, etc.
Insurance Copilot simplifies the task by allowing an insurance agent and the client to understand an insurance scheme in plain English, know the most critical points, and query the document.

## Tech stack
Frontend: nodeJS
Backend: python, uAgents, FastAPI
AI services: GPT-4o

## Instructions to run the project

### Env setup

Install packages:
`pip install -r requirements.txt`

To access each agent, run the following command:
`python agents/<agent_name>.py`

Create an OpenAI account and generate your own API key from https://platform.openai.com/api-keys
You will need to add funds to your account to use GPT4o.

Create a .env file in the main directory and add your OpenAI API key:
OPENAI_API_KEY = 'INSERT_KEY_HERE'


## Use cases
### Parsing agent
Parses document and provides a document summary:
- Run `python agents/parsing_agent.py`

### Questions agent
Generates 10 suggested questions that users might have about the document:
- Run `python agents/qna_agent.py`

### Recommendation agent
Answers a question in the context of given user data:
- Run `python agents/rec_agent.py`



## Special considerations, if any
<TODO>
