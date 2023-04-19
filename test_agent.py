import os
os.environ["OPENAI_API_KEY"] = "sk-"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_Rpsd"
os.environ["COHERE_API_KEY"] = "MYyesFr5qANJ"
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceHub, Cohere
from langchain import LLMMathChain, SerpAPIWrapper
tools = [
    Tool(
        name="apply for leave",
        func=lambda x: "已经成功帮你申请请假", #Mock Function
        description="apply for leave",
    ),
    Tool(
        name="None",
        func=lambda x: "你好",
        description="when there is no question",
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
agent.run(input="我想请假")
