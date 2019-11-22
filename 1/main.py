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

#endpoints

wrnd_endpoint="/words/randomWord?api_key={0}".format(api_key)
weg_endpoint="/word/{0}/examples?api_key={1}".format(word,api_key)
wrel_endpoint="/word/{0}/relatedWords?api_key={1}".format(word,api_key)

def word_definition(word): 
    wdef_endpoint="/word/{0}/definitions?api_key={1}".format(word,api_key)
    f_url = url+wdef_endpoint
    
    r = requests.get(url = f_url)
    
    return r.json(),r.status_code
    
def main():
    data,status = word_definition("field")
    if status == 200: 
        for i in data:
            print(i['text'])

main()
    
    








