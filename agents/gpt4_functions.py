# API interface with open ai
import openai
import logging
from openai import OpenAI
from dotenv import load_dotenv
import os

openai._utils._logs.logger.setLevel(logging.WARNING)
openai._utils._logs.httpx_logger.setLevel(logging.WARNING)

# Test openAI connection

def completion_test():

	load_dotenv()  # This loads the environment variables from .env
	db_user = os.getenv("DB_USER")
	client = OpenAI()

	completion_test = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content": "You are a concise assistant."},
			{"role": "user", "content": "Name 5 fruits."}
		]
	)

	print(completion_test.choices[0].message)

# Create client (manage communication to openAI API)

def create_client():
	load_dotenv()  # This loads the environment variables from .env
	db_user = os.getenv("DB_USER")
	client = OpenAI()

	return client

# client = create_client()

# Create assistant (an instance of a chat box)

name = "Insurance Paralegal"
assistant_desc = "You are an expert paralegal analyst. Use your knowledge base to answer questions about the provided pension insurance documents."

def create_assistant(client, assistant_name, assistant_desc, gpt_model):

	assistant = client.beta.assistants.create(
		name=assistant_name,
		instructions=assistant_desc,
		model=gpt_model,
		tools=[{"type": "file_search"}],
	)

	return assistant

# assistant = create_assistant(client, name, assistant_desc, 'gpt-4o')

prompt = """
		Summarize the provided document in 3 sentences, as if you would to an insurance attorney who is familiar with insurance related legal terms.
		Then provide 3 to 10 key bullet points that capture the most critical rules.
		Use only the latest provided document as your ground truth. Ignore all previous documents.
"""

# Upload a file

filepaths = ["agents/IBP_Problemstatement.docx"]

def upload_file(client, assistant, filepaths):

	# Create a vector store caled "Insurance Statements"
	vector_store = client.beta.vector_stores.create(name="Insurance Statements")
	
	# Ready the files for upload to OpenAI
	file_paths = filepaths
	file_streams = [open(path, "rb") for path in file_paths]
	
	# Use the upload and poll SDK helper to upload the files, add them to the vector store,
	# and poll the status of the file batch for completion.
	file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
		vector_store_id=vector_store.id, files=file_streams
	)
	
	# You can print the status and the file counts of the batch to see the result of this operation.
	# print(file_batch.status)
	# print(file_batch.file_counts)

	assistant = client.beta.assistants.update(
		assistant_id=assistant.id,
		tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
	)

	# Upload the user provided file to OpenAI
	message_file = client.files.create(
		file=open("agents/IBP_Problemstatement.docx", "rb"), purpose="assistants"
	)

	return message_file

# message_file = upload_file(client, assistant, filepaths)

# Prompt a question regarding the last file uploaded

def prompt_gpt4(client, assistant, prompt):

	# Retrieve the list of files already uploaded and get the ID of the latest file
	files_list = client.files.list()
	print(files_list.data)
	latest_file_id = files_list.data[-1].id  # Get the ID of the last uploaded file

	# Create a thread and attach the latest uploaded file to the message
	thread = client.beta.threads.create(
		messages=[
			{
				"role": "user",
				"content": prompt,
				# Attach the latest uploaded file to the message
				"attachments": [
					{"file_id": latest_file_id, "tools": [{"type": "file_search"}]}
				],
			}
		]
	)
 
	# The thread now has a vector store with that file in its tool resources.
	# print(thread.tool_resources.file_search)

	run = client.beta.threads.runs.create_and_poll(
			thread_id=thread.id, assistant_id=assistant.id
	)

	messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

	if len(messages) == 0:
		print("No messages in thread.")
		return

	message_content = messages[0].content[0].text
	annotations = message_content.annotations
	citations = []
	for index, annotation in enumerate(annotations):
		message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
		if file_citation := getattr(annotation, "file_citation", None):
			cited_file = client.files.retrieve(file_citation.file_id)
			citations.append(f"[{index}] {cited_file.filename}")

	# print(message_content.value)
	# print("\n".join(citations))

	return message_content.value, "\n".join(citations)

# response, citations = prompt_gpt4(client, assistant, prompt)

# print(response)
# print(citations)

# Optional: clear all files from a specified client (does not clear other clients)

def clear_all_files(client):

	try:
		# Retrieve a list of all files
		files = client.files.list()

		# Loop through the list of files and delete each one
		for file in files.data:
			# Delete the file using its ID
			client.files.delete(file_id=file.id)
			print(f"Deleted file with ID: {file.id}")

		print("All files have been deleted.")

	except Exception as e:
		print(f"An error occurred: {e}")

def clear_all_vector_stores(client):
	try:
		# Retrieve a list of all vector stores
		vector_stores = client.beta.vector_stores.list()

		# Loop through the list of vector stores and delete each one
		for vector_store in vector_stores.data:
			# Delete the vector store using its ID
			client.beta.vector_stores.delete(vector_store_id=vector_store.id)
			print(f"Deleted vector store with ID: {vector_store.id}")

		print("All vector stores have been deleted.")

	except Exception as e:
		print(f"An error occurred: {e}")

# clear_all_files(client)
# clear_all_vector_stores(client)