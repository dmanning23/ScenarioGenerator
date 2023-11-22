import os
import streamlit as st
from openai import OpenAI
#from keys import openAIapikey
import json
import random
import sys
from Generators.settingGenerator import SettingGenerator
from Generators.locationGenerator import LocationGenerator
from Simulation.location import Location

def generate_setting(locations, characters):
    response = ""
    response + f"{generate_locations(locations)}\n\n"
    response + f"{generate_characters(characters)}\n\n"
    return response

def generate_characters(characters):
    response = ""
    for character in characters:
        response + f"{generate_character(**character)}\n\n"
    return response

def generate_character(name, age, gender, personality):
    return f"{name} is a {age} years old {gender}.\n{personality}"

def generate_locations(locations):
    response = ""
    for location in locations:
        response + f"{generate_location(**location)}\n\n"
    return response

def generate_location(name, description):
    return f"{name}:\n{description}"

def printResponse(response_message):
    if response_message.function_call:
        #Which function call was invoked?
        function_called = response_message.function_call.name
        
        #Extract the arguments from the AI payload
        function_args  = json.loads(response_message.function_call.arguments)
        
        #Create a list of all the available functions
        available_functions = {
            "generate_setting": generate_setting,
            #TODO add more functions here?
        }
        
        fuction_to_call = available_functions[function_called]

        #Call the function with the provided arguments
        response_message = fuction_to_call(*list(function_args.values()))
    else:
        #The LLM didn't call a function but provided a response
        response_message = response_message.content
    #Write the response
    st.subheader(response_message)

def writeLocation(location, generator, level = 0):
    st.header(f"{level}: {location.describe()}")
    if location.locations:
        level = level + 1
        st.subheader(f"Child locations of {location.name}:")
        for child in location.locations:
            writeLocation(child, generator, level)

def recursionTest():
    #Get the user's input
    container = st.container()
    with container:
        with st.form(key="my form", clear_on_submit=True):
            user_input  = st.text_area(label="Enter a location description: ", key="input", height = 100)
            submit_button = st.form_submit_button(label="Can subdivide?")

        if submit_button:
            descriptions = []
            if user_input:
                descriptions.append(user_input)
            else:
                #If the user doesn't enter any input, use a default prompt
                descriptions.append(Location("Training Grounds", "Open spaces surrounded by trees where ninjas practice martial arts, stealth techniques, and engage in sparring sessions."))
                descriptions.append(Location("Small Huts", "A group of huts."))
                descriptions.append(Location("Apartment building", "A multi-tenant building with many apartments."))
                descriptions.append(Location("Main square", "The heart of the village, full of small shops and cafes."))
                descriptions.append(Location("Cozy cottages", "Tiny, picturesque homes with thatched roofs and blooming gardens."))
                descriptions.append(Location("Local pub", "A warm and friendly watering hole where villagers gather for drinks and conversation."))
                descriptions.append(Location("Country market", "A bustling market where artisans and farmers sell their wares."))

            with st.spinner("Thinking..."):
                for description in descriptions:
                    #output the user's prompt
                    st.header(description.describe())

                    #create the initial list of locations
                    generator = LocationGenerator()
                    canSubdivide = generator.CanSubdivide(description, OpenAI())
                    st.subheader(canSubdivide)

def main():
    #Get the user's input
    container = st.container()
    with container:
        with st.form(key="my form", clear_on_submit=True):
            user_input  = st.text_area(label="Enter a short description of the setting: ", key="input", height = 100)
            submit_button = st.form_submit_button(label="Generate")

        client = OpenAI()
        if submit_button:
            descriptions = []
            if user_input:
                descriptions.append(user_input)
            else:
                #If the user doesn't enter any input, use a default prompt
                descriptions.append(f"A cozy little village")
                
            with st.spinner("Thinking..."):
                for description in descriptions:
                    #output the user's prompt
                    st.markdown(description)

                    #expand the setting
                    settingGen = SettingGenerator()
                    setting = settingGen.Generate(description)
                    st.markdown(setting)

                    #create the various locations
                    #create the initial list of locations
                    locationGen = LocationGenerator()
                    locations = locationGen.Generate(description)

                    #decompose each location into children if application
                    for location in locations:
                        locationGen.GenerateChildLocations(location)
                        writeLocation(location, locationGen)

if __name__ == "__main__":

    #Set up the api key for OpenAI
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    #os.environ["OPENAI_API_KEY"] = openAIapikey

        #Initialize the Streamlit page
    st.set_page_config(
        page_title="Character List Generator",
        page_icon="🏘")

    #recursiontTest()
    main()