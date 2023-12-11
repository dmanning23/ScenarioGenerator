from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from Simulation.setting import Setting
from Generators.locationGenerator import LocationGenerator

class SettingGenerator:

    def Generate(self, description, llm = None):
        if llm is None:
            llm = ChatOpenAI()
        messages = [
            SystemMessage(content="Expand the following description of a setting."),
            HumanMessage(content=description),]
        result = llm.invoke(messages)
        return Setting(description, result.content)
    
    def GenerateLocations(self, setting, llm= None):
        locationGen = LocationGenerator()
        self.locations = locationGen.Generate(setting.name)