import re




def get_structures(prompt):
    """
    function contains break down of the info in the prompt , we have 4 sections 
    the steps section is an array , the final sections of the entities 
    the final obj is entities , it has 4 lists of the entite and its def
    
    """
    text=prompt.replace("text","video")
    print(prompt)
    summary_dict={}
    sections=text.split("Goal:")
    sections=sections[1].split("Global Understanding:")
    summary_dict["goal"]=sections[0]
    sections=sections[1].split("Steps:")
    summary_dict["global_understanding"]=sections[0]
    sections=sections[1].split("Entity Extraction:")
    summary_dict["steps"]=sections[0]
    summary_dict["entities"]=sections[1]
    return summary_dict
        

def get_steps(steps):
     splited=steps.split("**")
     if len(splited)<2:
      return ["This video contain no clear steps"]
     return splited[1:]
         

def get_entities(entities):
    splitted=entities.split("*")
    splitted=[x for x in splitted if x.strip()!=""]
    splitted=[x.split(":") for x in splitted]
    
    return splitted


def prompt_2_json(prompt):
    """
    function contains break down of the info in the prompt , we have 4 sections 
    the steps section is an array , the final sections of the entities 
    the final obj is entities , it has 4 lists of the entite and its def
    
    """
    summary_dict=get_structures(prompt)
    summary_dict["steps"]=get_steps(summary_dict["steps"])
    summary_dict["entities"]=get_entities(summary_dict["entities"])
    return summary_dict
    