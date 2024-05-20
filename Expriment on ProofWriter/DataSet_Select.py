import os
import logging
import datetime
import json
from typing import Dict, List, Callable, Union

def data_loader():
    data = []
    or_data = []
    counter = 0
    # open the original abduction dataset
    with open('meta-abduct-train-depth-0.jsonl', 'r') as file:
        for line in file:
            json_object = json.loads(line)
            or_data.append(json_object)
            
    # parse the dataset and split the triples and rules
    selected_data = or_data
    for json_object in selected_data:
        new_json = {}
        triples = json_object["triples"]
        rules = json_object["rules"]
        ab = json_object["abductions"]
        ts = []
        rs = []
        abduction = ""
        ans = ""
        # for triples
        for key, value in triples.items():
            ts.append(value["text"])
        # for rules
        for key, value in rules.items():
            rs.append(value["text"])
        # check if the triples and rules are enough
        if len(ts) < 10 or len(rs) < 3:
            continue
        # for abduction and ans
        for key, value in ab.items():
            if len(value["answers"])!=0:
                abduction = value["question"]
                alist = value["answers"]
                ans = alist[0]["text"]
                break
        # check if the abduction and ans are not None or blank
        if abduction == '' or ans == '':
            continue
        new_json["Premises"] = ts
        new_json["Rules"] = rs
        new_json["Phenomenon"] = abduction
        new_json["Hypothesis"] = ans
        new_json["Label"] = 'True'
        data.append(new_json)
        if len(data) >= 50:
            break
    return data
    
if __name__ == "__main__":

    data = data_loader()
    
    with open('proofwriter_dataset_changed.jsonl', 'a', encoding='utf-8') as file:
        for json_str in data:
            file.write(json.dumps(json_str) + '\n')
  
