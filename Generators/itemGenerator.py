from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
import json
from Simulation.item import Item
from openai import OpenAI
from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from Generators.finiteStateMachineGenerator import FiniteStateMachineGenerator

class ItemGenerator():

    generateItemsFunctionDef = {
            'name': 'generate_items',
            'description': 'Create a list of items',
            'parameters': {
                "type": "object",
                "properties": {
                    "items": {
                        'type': 'array',
                        "description": "A list of items",
                        "items": {
                            "type": "object",
                            "description": "A single item",
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'description': 'Name of the item'
                                },
                                'description': {
                                    'type': 'string',
                                    'description': "A description of the location."
                                },
                                'hasFiniteStateMachine': {
                                    'type': 'boolean',
                                    'description': 'True if this is an item that can be represented by a finite state machine and have more than one state, False otherwise',
                                },
                                'canBePickedUp': {
                                    'type': 'boolean',
                                    'description': "True if this is an item that could be picked up and added to a player's inventory, False otherwise",
                                }
                            },
                            "required": ["name", "description"]
                        },
                    },
                },
                "required": ["items",]
            }
    }

    def _generate_items(self, items):
        response = []
        for item in items:
            response.append(self._generate_item(**item))
        return response

    def _generate_item(self, name, description, hasFiniteStateMachine = False, canBePickedUp = False):
        return Item(name, description, hasFiniteStateMachine, canBePickedUp)

    def _parseResponse(self, response_message):
        if response_message.function_call and response_message.function_call.arguments:
            #Which function call was invoked?
            function_called = response_message.function_call.name
            
            #Extract the arguments from the AI payload
            function_args  = json.loads(response_message.function_call.arguments)
            
            #Create a list of all the available functions
            available_functions = {
                "generate_items": self._generate_items,
            }
            
            fuction_to_call = available_functions[function_called]

            #Call the function with the provided arguments
            return fuction_to_call(*list(function_args.values()))
        else:
            #The LLM didn't call a function but provided a response
            #return response_message.content
            return None

    def Generate(self, description, llm = None):
        if llm is None:
            llm = ChatOpenAI()
        messages = [
            SystemMessage(content="Expand the following description of an item."),
            HumanMessage(content=description),]
        result = llm.invoke(messages)
        return result.content
    
    def GenerateItems(self, location, llm = None):
        if not llm:
            #create the client API
            llm = OpenAI()

        messages = [
            {'role': 'system', 'content': "Given the following name and description of a location, generate a list of items that can be found at that location."},
            {'role': 'user', 'content': f"{location.name}: {location.description}"}
        ]

        #Create the list of function definitions that are available to the LLM
        functions = [ ItemGenerator.generateItemsFunctionDef ]

        #Call the LLM...
        response = llm.chat.completions.create(
            model = 'gpt-3.5-turbo',
            temperature=1,
            messages = messages,
            functions = functions, #Pass in the list of functions available to the LLM
            function_call = 'auto')
        items = self._parseResponse(response.choices[0].message)
        if items is None:
            return [] #if it gets here, there was a problem with the description
        else:
            return items
        
    def GenerateFiniteStateMachine(self, item, llm = None):
        if item.canInteract:
            fsmGen = FiniteStateMachineGenerator()
            item.stateMachine = fsmGen.GenerateStateMachine(item.name)
