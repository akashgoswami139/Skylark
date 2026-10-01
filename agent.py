from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import get_weather, city_details
from langchain_core.messages import HumanMessage, SystemMessage
from prompt import SYSTEM_PROMPT
load_dotenv



load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


tools = {
    "get_weather" : get_weather,
    "city_details" : city_details

}




message = []


llm_tools= llm.bind_tools(
    [
        get_weather,
        city_details
    ]
)



class Agent:

    def __init__(self, city: str):
        self.city = city

    def run(self):

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=self.city)
        ]

        result = llm_tools.invoke(messages)

        # Add AI message containing tool call
        messages.append(result)

        if result.tool_calls:

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                tool_result = tools[tool_name].invoke(tool_call)

                messages.append(tool_result)

        # Ask LLM to generate final response
        final_result = llm_tools.invoke(messages)

        return final_result.content

