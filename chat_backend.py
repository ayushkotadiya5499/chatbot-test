from langchain.agents import create_agent
from langgraph.graph.state import StateGraph,START,END
from langgraph.graph.message import add_messages ,BaseMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict,Annotated,List
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage,AIMessage
from langchain_perplexity.chat_models import ChatPerplexity
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "test.db")

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)
checkpointer=SqliteSaver(conn=conn)
config={'configurable':{'thread_id':'th'}}

api_key=os.getenv('PERPLEXITY_API_KEY')

model=ChatPerplexity(api_key=api_key)

agent=create_agent(model=model)

class chat_bot(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_with_bot(state:chat_bot):
    question=state['messages']
    response=model.invoke(question)
    return {'messages':[response]}

graph=StateGraph(chat_bot)

graph.add_node('chat_with_bot',chat_with_bot)

graph.add_edge(START,'chat_with_bot')
graph.add_edge('chat_with_bot',END)


wrokflow=graph.compile(checkpointer=checkpointer)

