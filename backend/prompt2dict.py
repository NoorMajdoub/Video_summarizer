import re


def get_entities(splited):
    entities={}
    for i in range(10,17,2):
       
        temp=splited[i].split("*")
        for i in range(1,len(temp)-1):
            entity_def=temp[i].split(":")
          
            if len(entity_def>2):
             entities[entity_def[0]]=entity_def[1]
    return entities
def prompt_2_json(prompt):
    splited=prompt.split("**")
    summary_dict={}
    summary_dict["Goal"]=splited[2].replace(":","").replace("0-9","")
    summary_dict["Global Understanding"]=splited[4].replace(":","").replace("0-9","")
    summary_dict["Steps"]=splited[6].replace(":","").replace("0-9","")
    entities=get_entities(splited)
    summary_dict["Entities"]=entities
    return summary_dict
    