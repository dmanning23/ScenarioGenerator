from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI

class SettingGenerator:

    def Generate(self, description, llm = None):
        if llm is None:
            llm = ChatOpenAI()
        messages = [
            SystemMessage(content="Expand the following description of a setting."),
            HumanMessage(content=description),]
        result = llm.invoke(messages)
        return result.content