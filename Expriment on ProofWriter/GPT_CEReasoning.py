import os
import logging
import datetime
import json
from typing import Dict, List, Callable, Union
import openai

openai.api_key = 'Your OpenAI API Key' 

def get_completion(prompt, model="gpt-4-turbo", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
    
def get_messages(messages, model="gpt-4-turbo", temperature=1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

FOL_prompt_1 = """Suppose you are one of the greatest AI scientists, logicians and mathematicians. Let us think step by step. Read the "Premises" first, then using First-Order Logic to judge whether the "Hypothesis" is True. Please make sure your reasoning is directly deduced from given information other than introducing unsourced common knowledge and unsourced information by common sense reasoning.
---
"Premises": 
{premises}
"Hypothesis": {hypothesis}
"""

FOL_prompt_2 = """Please output your answer with {"Judgement":True or False or Unknown,"Reason":Your reason}.Please only output the json without any other context.
"""

def data_loader():
    data = []
    with open('clear_proofwriter_dataset_changed.jsonl', 'r') as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data
    
def FOL(data):
    logs = []
    counter = 0
    correct_ans = 0
    for djson in data:
        input_text = ""
        p_list = djson["Premises"]
        r_list = djson["Rules"]
        L = djson["Label"]
        input_text += "\""+djson["Hypothesis"]+"\"\n"
        for i in p_list:
            input_text += "\""+i+"\"\n" 
        for i in r_list:
            input_text += "\""+i+"\"\n" 
        prompt = FOL_prompt_1.format(premises = input_text,hypothesis = djson["Phenomenon"])
        ans = get_completion(prompt)
        p = FOL_prompt_2
        messages = [{"role": "user", "content": prompt},{"role": "assistant", "content": ans},{"role": "user", "content": p}]
        ans = get_messages(messages)
        aa = ans.split(',')
        counter = counter + 1
        if L == "True" and aa[0].count('rue'):
            correct_ans = correct_ans + 1
        elif L == "False" and aa[0].count('lse'):
            correct_ans = correct_ans + 1
        logs.append(ans)
    return logs,correct_ans,counter     
    
if __name__ == "__main__":
    data = data_loader()
    
    logs_FOL,c,a = FOL(data[0:200])
    
    json_strings = [json.dumps(item) for item in logs_FOL]

    Set = "ProofWriter"
    
    Model = "GPT4"

    file_path_FOL = Model + "_Logs_CE_" + Set + ".txt"
    
    file_path = Model + "_Correct_CE_" + Set + ".txt"

    with open(file_path_FOL, "w") as file:
        for json_str in json_strings:
            file.write(json_str + '\n')
            
    with open(file_path, "w") as file:
        file.write('Correct:'+ str(c) + '  Total:' + str(a) + '\n')