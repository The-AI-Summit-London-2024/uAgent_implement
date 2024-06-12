from uagents import Agent, Bureau, Context, Model
from PyPDF2 import PdfReader

class Message(Model):
    message: str

parsing = Agent(name="parsing", seed="documents parsing")


def read_file():
    file_path = input("Enter file_path: ")

@parsing.on_event("startup")
async def get_pdf(ctx: Context):
    read_file()


bureau = Bureau()
bureau.add(parsing)

if __name__ == "__main__":
    bureau.run()
