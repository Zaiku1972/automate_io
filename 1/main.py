# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:11:56 2019

@author: sriram1204
"""
import random
"""for RestCall """
import requests
"""For commandline"""
import os

#params or definitions
url="https://fourtytwowords.herokuapp.com"
api_key="b972c7ca44dda72a5b482052b1f5e13470e01477f3fb97c85d5313b3c112627073481104fec2fb1a0cc9d84c2212474c0cbe7d8e59d7b95c7cb32a1133f778abd1857bf934ba06647fda4f59e878d164"
FAILED_CONSTANT = "requested_failed"

#helper functions
def response_data(raw_response_data): 
    data = dict()
    data['status'] = raw_response_data.status_code
    data['data'] = raw_response_data.json()
    
    return data
def requester(endpoint): 
    f_url = url+endpoint
    raw_response_data = requests.get(url = f_url)
    f_data = response_data(raw_response_data)
    return f_data

#api functions        
def word_random(): 
    wrnd_endpoint="/words/randomWord?api_key={0}".format(api_key)
    data = requester(wrnd_endpoint)
    if(data['status'] == 200): 
        return data['data']['word']
    else:
        return FAILED_CONSTANT
    
def word_definition(word): 
    wdef_endpoint="/word/{0}/definitions?api_key={1}".format(word,api_key)
    data = requester(wdef_endpoint)
    
    definition = list()
    
    if(data['status'] == 200): 
        for i in data['data']:
            definition.append(i['text'])
    else: 
        definition.append('No Definitions')
        
    return definition

def word_ant(word): 
    wrel_endpoint="/word/{0}/relatedWords?api_key={1}".format(word,api_key)
    data = requester(wrel_endpoint)
    
    if(data['status'] == 200): 
        for i in data['data']:
            if(i['relationshipType'] == "antonym"): 
                return i["words"]
    else: 
        return list()           

def word_syn(word): 
    wrel_endpoint="/word/{0}/relatedWords?api_key={1}".format(word,api_key)
    data = requester(wrel_endpoint)
    
    if(data['status'] == 200): 
        for i in data['data']:
            if(i['relationshipType'] == "synonym"): 
                return i["words"]
    else: 
        return list()           
    
def word_example(word): 
    weg_endpoint="/word/{0}/examples?api_key={1}".format(word,api_key)
    data = requester(weg_endpoint)
    example = list()
    
    if(data['status'] == 200): 
        print("Examples\n")
        for i in data['data']['examples']:
            example.append(i['text'])
            print(i['text'])
            print("\n")
    else: 
        example.append('No Examples')
        print('No Examples\n')
    

def word_full(word): 
    definitions = word_definition(word)
    ant = word_ant(word)
    syn = word_syn(word)
    eg = word_example(word)
    
    print("{0}\n{1}\n{2}\n{3}".format(definitions,ant,syn,eg))

def word_of_the_day(): 
    word = word_random()
    
    if(word != FAILED_CONSTANT): 
        word_full(word)
    
    else: 
        print("No Word for the day")

def shuffleWord(word): 
    tempWord = list(word)
    random.shuffle(tempWord)
    return ''.join(tempWord)
    
def validateAnswer(word,syn):
    answer = str(input("The Word is?:")).lower()
    if(answer == word or answer in syn): 
        return True
    return False

def showHints(word,definitions,ant,syn,comingBack=False): 
    
    if(comingBack): 
        print("Jumbled Form of Word:{}".format(shuffleWord(word)))
        
    if(len(definitions) > 0): 
        randomChoice = random.randint(0,len(definitions) - 1)
        print("Definition:Clue")
        print(definitions[randomChoice])
        del definitions[randomChoice]
    
    if(len(syn) > 0 and len(ant) > 0):
        choice = random.randint(0,1)
        
        if(choice == 0):
            print("Syn:Clue")
            randomChoice = random.randint(0,len(syn) -1) 
            print(syn[randomChoice])
            del syn[randomChoice]

        if(choice == 1):
            print("Ant:Clue")
            randomChoice = random.randint(0,len(ant) - 1) 
            print(ant[randomChoice])
            del ant[randomChoice]

    
    elif(len(syn) > 0 and len(ant) == 0):
        print("Syn:Clue")
        randomChoice = random.randint(0,len(syn) - 1) 
        print(syn[randomChoice])
        del syn[randomChoice]
        
    elif(len(ant) > 0 and len(syn) == 0):
        print("Ant:Clue")
        randomChoice = random.randint(0,len(syn) - 1) 
        print(ant[randomChoice])
        del randomChoice
    
def word_play(): 
    word = word_random()
    definitions = word_definition(word)
    ant = word_ant(word)
    syn = word_syn(word)
    eg = word_example(word)
    
    showHints(word,definitions,ant,syn,comingBack=False)
    result = validateAnswer(word,syn) 
    
    while(result != True): 
        print("\n Wrong Answer")
        print("\n1-Try Again\n2-Hint\n3-Quit")
        choice = int(input("Enter Choice:"))
        
        if(choice == 1): 
            result = validateAnswer(word,syn)
        
        if(choice == 2): 
            showHints(word,definitions,ant,syn,comingBack=True)
            result = validateAnswer(word,syn)
            
        if(choice == 3):
            print("Word is:{}".format(word))
            break
        
        if(choice > 3): 
            print("Wrong Choice")
            continue
        
        
    
    
    








