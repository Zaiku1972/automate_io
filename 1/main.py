# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:11:56 2019

@author: sriram1204
"""
import random
"""for RestCall """
import requests
"""For commandline"""
import sys

"""Global Params Definition"""
url="https://fourtytwowords.herokuapp.com"
api_key="b972c7ca44dda72a5b482052b1f5e13470e01477f3fb97c85d5313b3c112627073481104fec2fb1a0cc9d84c2212474c0cbe7d8e59d7b95c7cb32a1133f778abd1857bf934ba06647fda4f59e878d164"
FAILED_CONSTANT = "requested_failed"


def response_data(raw_response_data): 
    """Response Data Formation Function"""
    data = dict()
    data['status'] = raw_response_data.status_code
    data['data'] = raw_response_data.json()
    
    return data

def requester(endpoint): 
    """Resquest Data Function """
    f_url = url+endpoint
    raw_response_data = requests.get(url = f_url)
    f_data = response_data(raw_response_data)
    return f_data

#api functions        
def word_random(): 
    """Request Random Word"""
    wrnd_endpoint="/words/randomWord?api_key={0}".format(api_key)
    data = requester(wrnd_endpoint)
    if(data['status'] == 200): 
        return data['data']['word']
    else:
        return FAILED_CONSTANT
    
def word_definition(word):
    """Get Definition for a word """
    wdef_endpoint="/word/{0}/definitions?api_key={1}".format(word,api_key)
    data = requester(wdef_endpoint)
    
    definition = list()
    
    if(data['status'] == 200): 
        for i in data['data']:
            definition.append(i['text'])
    else: 
        definition.append('No Definitions for the word'.format(word))
        
    return definition

def word_ant(word): 
    """Get Antonmy for a word"""
    wrel_endpoint="/word/{0}/relatedWords?api_key={1}".format(word,api_key)
    data = requester(wrel_endpoint)
    
    if(data['status'] == 200): 
        for i in data['data']:
            if(i['relationshipType'] == "antonym"): 
                return i["words"]
        return list()
    else: 
        return list()           

def word_syn(word): 
    """Get Synonm for a word"""
    wrel_endpoint="/word/{0}/relatedWords?api_key={1}".format(word,api_key)
    data = requester(wrel_endpoint)
    
    if(data['status'] == 200): 
        for i in data['data']:
            if(i['relationshipType'] == "synonym"): 
                return i["words"]
        return list()
    else: 
        return list('')           
    
def word_example(word): 
    """Get Example for a word """
    weg_endpoint="/word/{0}/examples?api_key={1}".format(word,api_key)
    data = requester(weg_endpoint)
    example = list()
    
    if(data['status'] == 200): 
        for i in data['data']['examples']:
            example.append(i['text'])
    else: 
        example.append('No Examples')
    
    return example    

def word_full(word): 
"""Display all Params of the given Word """
    print("Defn\n")
    for i in word_definition(word):
        print(i)
                
    print("Syn:\n")
    for i in word_syn(word): 
        print(i)
                
    print("Ant:\n")
    for i in word_ant(word):
        print(i)
        
    print("Exampes\n")
    for i in word_example(word):
        print(i)
    
    

def word_of_the_day(): 
    """Display all params of a random word """
    word = word_random()
    
    if(word != FAILED_CONSTANT): 
        print("Word of the day {}".format(word))
        word_full(word)
    
    else: 
        print("No Word for the day")

def shuffleWord(word): 
    """Shuffle a Given word in any order """
    tempWord = list(word)
    random.shuffle(tempWord)
    return ''.join(tempWord)
    
def validateAnswer(word,syn):
    """Check function for the final answer """
    answer = str(input("The Word is?:")).lower()
    if(answer == word or answer in syn): 
        return True
    return False

def showHints(word,definitions,ant,syn,comingBack=False): 
#state of variable has to be maintained,only for word play
    """ Display Hint for the Play Function"""
    if(comingBack): 
        print("Jumbled Form of Word:{}".format(shuffleWord(word)))
        
    if(len(definitions) > 0): 
        randomChoice = random.randint(0,len(definitions) - 1)
        print("Definition:Clue")
        print(definitions[randomChoice])
        
    
    if(len(syn) > 0 and len(ant) > 0):
        choice = random.randint(0,1)
        
        if(choice == 0):
            print("Syn:Clue")
            randomChoice = random.randint(0,len(syn) -1) 
            print(syn[randomChoice])
            

        if(choice == 1):
            print("Ant:Clue")
            randomChoice = random.randint(0,len(ant) - 1) 
            print(ant[randomChoice])
            

    
    elif(len(syn) > 0 and len(ant) == 0):
        print("Syn:Clue")
        randomChoice = random.randint(0,len(syn) - 1) 
        print(syn[randomChoice])
        
        
    elif(len(ant) > 0 and len(syn) == 0):
        print("Ant:Clue")
        randomChoice = random.randint(0,len(syn) - 1) 
        print(ant[randomChoice])
        
    
def word_play(): 
    """Play Function"""
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
    
def main():
    """Command Line Function"""
    if(len(sys.argv) > 3):
        print("Execute with one params and one arg,for eg\n1- defn <word>\n2- syn<word>\n3- ant<word>\n4- ex<word>\n5- <word>\n6- just execute\n7- play")
    
    if(len(sys.argv) == 3):
        func = sys.argv[1]
        word = sys.argv[2]
        
        if(func == 'defn'):
            print("Defn\n")
            for i in word_definition(word):
                print(i)
                
        if(func == 'syn'):
            print("Syn:\n")
            for i in word_syn(word): 
                print(i)
                
        if(func == 'ant'):
            print("Ant:\n")
            for i in word_ant(word):
                print(i)
        
        if(func == 'ex'):
            print("Examples\n")
            for i in word_example(word):
                print(i)
        
    if(len(sys.argv) == 2):
        param = sys.argv[1]
        if(param == 'play'):
            word_play()
        else:
            word_full(param)
            
    if(len(sys.argv) == 1):
        word_of_the_day()

main()