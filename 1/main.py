# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:11:56 2019

@author: sriram1204
"""
"""for RestCall """
import requests
"""For commandline"""
import os
#params or definitions
#word="field"
url="https://fourtytwowords.herokuapp.com"
api_key="b972c7ca44dda72a5b482052b1f5e13470e01477f3fb97c85d5313b3c112627073481104fec2fb1a0cc9d84c2212474c0cbe7d8e59d7b95c7cb32a1133f778abd1857bf934ba06647fda4f59e878d164"
FAILED_CONSTANT = "requested_failed"
#endpoints



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
            print("Definition\n")
            print(i['text'])
    else: 
        definition.append('No Definitions')
        print('No Definitions')

def word_syn_and_ant(word): 
    wrel_endpoint="/word/{0}/relatedWords?api_key={1}".format(word,api_key)
    data = requester(wrel_endpoint)
    
    f_dict = dict()
    if(data['status'] == 200): 
        for i in data['data']:
            f_dict[i['relationshipType']] = i['words']
            print(i['relationshipType'])
            print("\n")
            print(i['words'])
    else: 
        print("No Syn or Ant")            

def word_example(word): 
    weg_endpoint="/word/{0}/examples?api_key={1}".format(word,api_key)
    data = requester(weg_endpoint)
    example = list()
    
    if(data['status'] == 200): 
        for i in data['data']:
            example.append(i['text'])
            print("Examples\n")
            print(i['text'])
    else: 
        example.append('No Examples')
        print('No Examples')

def word_full(word): 
    word_definition(word)
    word_syn_and_ant(word)
    word_example(word)

def word_of_the_day(): 
    word = word_random()
    
    if(word != FAILED_CONSTANT): 
        word_full(word)
    
    else: 
        print("No Word for the day")

word_of_the_day()
    








