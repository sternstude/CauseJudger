import json
import random
 
Name = ['Gary','Peter','Ted','Adam','Bob','Charles','David','Denis','Eric','Frank','Henry',
        'Jack','James','Justin','Mark','Paul','Peter','Robert','Robin','Sandy','Thomas',
        'Tom','Anne','Betty','Grace','Helen','Jane','Jessica','Lisa','Lucy']

Adjectives = ["happy","angry","calm","excited","nervous","confident","shy","outgoing",
              "quiet","intelligent","curious","creative","honest","kind","generous",    
              "patient","brave","friendly","loyal","humorous","responsible","lazy",   
              "beautiful","wise","enthusiastic","mature","trustworthy","positive",
              "careless"]  

Template_1 = """If a person is {X1} and {Ab} then this person is {Target}"""

Template_2 = [
    """If a person is {X1} and {Ab} then this person is {T3}.""",
    """If a person is {T3} then this person is {Target}.""",          
]

Template_3 = [
    """If a person is {X1} and {Ab} then this person is {T3}.""",
    """If a person is {T3} then this person is {T4}.""",  
    """If a person is {T4} and {X5} then this person is {Target}.""",         
]

Template_4 = [
    """If a person is {X1} and {Ab} then this person is {T3}.""",
    """If a person is {T3} then this person is {T4}.""",  
    """If a person is {T4} then this person is {T5}.""",  
    """If a person is {T5} and {X6} then this person is {Target}.""",         
]

Random_1 = """If a person is {T1} then this person is {T2}."""

Random_2 = """If a person is {T1} and {T2} then this person is {T3}."""

def split_list_randomly(lst, n):  
    random.shuffle(lst)   
    size = 10 
    remainder = len(lst) % n
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def data_create():
    Target_Name = Name[random.randint(0, 29)]
    NoSense_Name = []
    while(1):
        index = random.randint(0, 29)
        if Name[index] != Target_Name:
            NoSense_Name.append(Name[index])
        if len(NoSense_Name)==4: break
    
    adj_tmp = Adjectives
    part_list = split_list_randomly(adj_tmp,3)
    L1 = part_list[0]
    L2 = part_list[1]
    L3 = part_list[2]
    # here to select the Level of Dataset (1-4)
    Template_Num = 4
    ##################
    Rules = []
    Premises = []
    Phenomenon = ""
    Hypothesis = ""
    Label = ""

    if Template_Num == 1:
        template = Template_1
        rule1 =template.format(X1=L1[0],Ab=L1[1],Target=L1[2])
        Rules.append(rule1)
        Phenomenon = Target_Name + " is " + L1[2]
        True_loc = random.randint(0, 9)
        Options = ["True","False"]
        Label = Options[True_loc>4]
        if Label == "True":
            Hypothesis = Target_Name + " is " + L1[1]
        else:
            Hypothesis = Target_Name + " is " + L3[1]
        Premises.append(Target_Name + " is " + L1[0])
        Premises.append(Target_Name + " is " + L1[3])
        for i in range(1,3):
            Rules.append(Random_1.format(T1=L3[random.randint(1, 4)],T2=L3[random.randint(4, 6)]))
        for i in range(1,3):
            Rules.append(Random_2.format(T1=L3[random.randint(1, 3)],T2=L3[random.randint(3, 5)],
                         T3=L3[random.randint(5, 7)]))
        for i in NoSense_Name:
            Premises.append(i + " is " + L1[random.randint(0, 3)])
            Premises.append(i + " is " + L1[random.randint(3, 6)])
            Premises.append(i + " is " + L1[random.randint(6, len(L1)-1)])

    elif Template_Num == 2:
        template = Template_2
        rule1 =template[0].format(X1=L1[0],Ab=L1[1],T3=L2[0])
        rule2 =template[1].format(T3=L2[0],Target=L1[2])
        Rules.append(rule1)
        Rules.append(rule2)
        Phenomenon = Target_Name + " is " + L1[2]
        True_loc = random.randint(0, 9)
        Options = ["True","False"]
        Label = Options[True_loc>4]
        if Label == "True":
            Hypothesis = Target_Name + " is " + L1[1]
        else:
            Hypothesis = Target_Name + " is " + L3[1]
        Premises.append(Target_Name + " is " + L1[0])
        Premises.append(Target_Name + " is " + L1[3])
        for i in range(1,3):
            Rules.append(Random_1.format(T1=L3[random.randint(1, 4)],T2=L3[random.randint(4, 6)]))
        for i in range(1,3):
            Rules.append(Random_2.format(T1=L3[random.randint(1, 3)],T2=L3[random.randint(3, 5)],
                         T3=L3[random.randint(5, 7)]))
        for i in NoSense_Name:
            Premises.append(i + " is " + L1[random.randint(0, 3)])
            Premises.append(i + " is " + L1[random.randint(3, 6)])
            Premises.append(i + " is " + L1[random.randint(6, len(L1)-1)])

    elif Template_Num == 3:
        template = Template_3
        rule1 =template[0].format(X1=L1[0],Ab=L1[1],T3=L2[0])
        rule2 =template[1].format(T3=L2[0],T4=L2[1])
        rule3 =template[2].format(T4=L2[1],X5=L1[3],Target=L1[2])
        Rules.append(rule1)
        Rules.append(rule2)
        Rules.append(rule3)
        Phenomenon = Target_Name + " is " + L1[2]
        True_loc = random.randint(0, 9)
        Options = ["True","False"]
        Label = Options[True_loc>4]
        if Label == "True":
            Hypothesis = Target_Name + " is " + L1[1]
        else:
            Hypothesis = Target_Name + " is " + L3[1]
        Premises.append(Target_Name + " is " + L1[0])
        Premises.append(Target_Name + " is " + L1[3])
        Premises.append(Target_Name + " is " + L1[4])
        for i in range(1,3):
            Rules.append(Random_1.format(T1=L3[random.randint(1, 4)],T2=L3[random.randint(4, 6)]))
        for i in range(1,3):
            Rules.append(Random_2.format(T1=L3[random.randint(1, 3)],T2=L3[random.randint(3, 5)],
                         T3=L3[random.randint(5, 7)]))
        for i in NoSense_Name:
            Premises.append(i + " is " + L1[random.randint(0, 2)])
            Premises.append(i + " is " + L1[random.randint(2, 4)])
            Premises.append(i + " is " + L1[random.randint(4, 6)])
            Premises.append(i + " is " + L1[random.randint(6, len(L1)-1)])

    elif Template_Num == 4:
        template = Template_4
        rule1 =template[0].format(X1=L1[0],Ab=L1[1],T3=L2[0])
        rule2 =template[1].format(T3=L2[0],T4=L2[1])
        rule3 =template[2].format(T4=L2[1],T5=L2[2])
        rule4 =template[3].format(T5=L2[2],X6=L1[3],Target=L1[2])
        Rules.append(rule1)
        Rules.append(rule2)
        Rules.append(rule3)
        Rules.append(rule4)
        Phenomenon = Target_Name + " is " + L1[2]
        True_loc = random.randint(0, 9)
        Options = ["True","False"]
        Label = Options[True_loc>4]
        if Label == "True":
            Hypothesis = Target_Name + " is " + L1[1]
        else:
            Hypothesis = Target_Name + " is " + L3[1]
        Premises.append(Target_Name + " is " + L1[0])
        Premises.append(Target_Name + " is " + L1[3])
        Premises.append(Target_Name + " is " + L1[4])
        for i in range(1,3):
            Rules.append(Random_1.format(T1=L3[random.randint(1, 4)],T2=L3[random.randint(4, 6)]))
        for i in range(1,3):
            Rules.append(Random_2.format(T1=L3[random.randint(1, 3)],T2=L3[random.randint(3, 5)],
                         T3=L3[random.randint(5, 7)]))
        for i in NoSense_Name:
            Premises.append(i + " is " + L1[random.randint(0, 2)])
            Premises.append(i + " is " + L1[random.randint(2, 4)])
            Premises.append(i + " is " + L1[random.randint(4, 6)])
            Premises.append(i + " is " + L1[random.randint(6, len(L1)-1)])

    random.shuffle(Rules)
    Ans = {"Premises":Premises,"Rules":Rules,"PossibleCause":Hypothesis,"Phenomenon":Phenomenon,"Label":Label}
    return Ans

if __name__ == "__main__":
    with open('YourDataSetName.jsonl', 'w', encoding='utf-8') as file: 
        for i in range(0,20000):
            data = data_create()
            file.write(json.dumps(data) + '\n')
