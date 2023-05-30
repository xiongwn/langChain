import os
import json
import requests
os.environ["OPENAI_API_KEY"] = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
os.environ["COHERE_API_KEY"] = "MYyesFr5qANJIB3ONOPK5MCqxZoHpu2ZD5D60cNU"
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceHub, Cohere, OpenAI
from langchain import LLMMathChain, SerpAPIWrapper

def post(paramString):
    response = requests.post(url = "https://v4pre.h5sys.cn/api/11231326/add", data = {"params": paramString}).json()
    return response
tools = [
    Tool(
        name="apply for leave",
        func=lambda x: "已经成功申请请假", #Mock Function
        description="apply for leave",
    ),
    Tool(
        name="None",
        func=lambda x: "你好",
        description="when there is no question",
    ),
    Tool(
        name="add",
        func=post,
        description="join many values.For example,join string 'a' and number 1,input `'a',1`.then accept the result",
    )
]
llm = ChatOpenAI(temperature=0)
# llm = Cohere()
# llm = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature":0, "max_length":64})
# print(ChatOpenAI(temperature=0))
# agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
# agent.run("what is the most famous song of christmas")
print("result",agent.run(input="帮我请假"))