# Run agents in background
python agents/parsing_agent.py &
python agents/qna_agent.py &
python agents/rec_agent.py &

# Run api service
python api_service.py

