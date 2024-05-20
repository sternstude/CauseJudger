import os
import logging
import datetime
import json
from typing import Dict, List, Callable, Union
import replicate
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
    
AB_prompt_1 = """Suppose you are one of the greatest AI scientists, logicians and mathematicians. Read the "Premises" and "Result", then judge whether the "Possible Cause" could cause the "Result". Please make sure your reasoning is directly deduced from given information other than introducing unsourced common knowledge and unsourced information by common sense reasoning.
---
"Premises": 
{premises}
"Result": {result}
"Possible Cause": {reason}
"""

AB_prompt_2 = """Please output the above answer with {"Judgement":True or False or Unknown,"Reason":Your reason}.Please only output the json without any other context. Please do not reasoning again, just summary the last answer.
"""

def data_loader():
    data = []
    with open('CauseLogics_Level_1.jsonl', 'r') as file:
        for line in file:
            json_object = json.loads(line)
            data.append(json_object)
    return data

def ABR(data):
    logs = []
    counter = 0
    correct_ans = 0
    for djson in data:
        input_text = ""
        p_list = djson["Premises"]
        r_list = djson["Rules"]
        for i in p_list:
            input_text += "\""+i+"\"\n" 
        for i in r_list:
            input_text += "\""+i+"\"\n" 
        hyps = djson["PossibleCause"]
        L = djson["Label"]
        resons = hyps
        prompt = AB_prompt_1.format(premises = input_text,result = djson["Phenomenon"],reason = resons)
        ans = get_completion(prompt)
        p = AB_prompt_2
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
 
    logs_ABR,c,a = ABR(data[0:100])
    
    json_strings = [json.dumps(item) for item in logs_ABR]

    Set = "Stage_1"
    
    Model = "GPT4"

    file_path_ABR = Model + "_Logs_IO_" + Set + ".txt"
    
    file_path = Model + "_Correct_IO_" + Set + ".txt"

    with open(file_path_ABR, "w") as file:
        for json_str in json_strings:
            file.write(json_str + '\n')
            
    with open(file_path, "w") as file:
        file.write('Correct:'+ str(c) + '  Total:' + str(a) + '\n')
    
