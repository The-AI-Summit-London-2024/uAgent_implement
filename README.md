# Insurance Copilot


## Description
Insurance companies frequently need to modify and customize pricing schemes (PRTs) for different clients to match their needs.
This takes considerable effort across multiple internal teams: legal, compliance, actuary, claims management, etc.

Insurance Copilot simplifies the task by allowing an insurance agent and the client to understand an insurance scheme in plain English, know the most critical points, and query the document.


## Tech stack
Frontend: nodeJS
Backend: python, uAgents, FastAPI
AI services: GPT-4o

Architecture Diagram:
![Architecture Diagram](images/archi_diagram.jpeg?raw=true)

## Instructions to run the project

### Env setup

In a Python virtual env, install packages:
`pip install -r requirements.txt`

Create an OpenAI account and generate your own API key from https://platform.openai.com/api-keys
You will need to add funds to your account to use GPT4o.

Create a `.env` file in the main directory and add your OpenAI API key:
```
OPENAI_API_KEY = 'INSERT_KEY_HERE'
```

To access each agent, run the following command:
`python agents/<agent_name>.py`

## Individual Agents
### Parsing agent
Parses a document and provides a summary of the document:
- Run `python agents/parsing_agent.py`

### Questions agent
Generates 10 suggested questions that users might have about the document, and identifies relevant sections of the document for each question:
- Run `python agents/qna_agent.py`

### Recommendation agent
Answers a question in the context of given user data (E.g an individual's age, gender, and marital status):
- Run `python agents/rec_agent.py`

## Combining all Agents
- Run `python api_service.py`

## TODOs
[NOTE]: The Recommendation agent has not been integrated into the combined app yet.

1. Full agent-to-agent integration
2. Final report output (PRT scheme) to meet key customer requirements
3. Host service on cloud
4. Integration with AgentVerse
5. Accuracy testing with more datasets and SMEs