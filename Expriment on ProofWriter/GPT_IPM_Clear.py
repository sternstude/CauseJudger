import os
import logging
import datetime
import json
from typing import Dict, List, Callable, Union
import openai

openai.api_key = 'Your OpenAI API Key' 

def get_completion(prompt, model="gpt-3.5-turbo", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
    
def get_messages(messages, model="gpt-3.5-turbo", temperature=1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
    
data_clear_prompt= """Suppose you are one of the greatest AI scientists, logicians and mathematicians. Please carefully read the following "Premises and Rules" and remove the facts that unrelated to {who}, and then output the new set of "Premises and Rules".
"Premises and Rules":{input}
"""
    
def data_loader():
    data = []
    with open('proofwriter_dataset_changed.jsonl', 'r') as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data
    
def data_clear(data):
    new_data = []
    for i in data:
        facts = i["Premises"]
        abd = i["Phenomenon"]
        oo = abd.split(" ")
        who = oo[0]
        prompt = data_clear_prompt.format(input = facts,who = who)
        ans = get_completion(prompt)
        ans = ans.replace("\'","")
        ans = ans.replace(", ",",")
        ans = ans.replace(" ,",",")
        ans = ans.replace("[","")
        ans = ans.replace("]","")
        i["Premises"] = ans.split(',')
        new_data.append(i)
    return new_data
        

if __name__ == "__main__":
    data = data_loader()
    new_data = data_clear(data[0:200])

    with open('clear_proofwriter_dataset_changed.jsonl', 'w', encoding='utf-8') as file:
        for json_str in new_data:
            file.write(json.dumps(json_str) + '\n')