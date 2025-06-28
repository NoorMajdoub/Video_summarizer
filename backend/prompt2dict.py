import re




def get_structures(prompt):
    """
    function contains break down of the info in the prompt , we have 4 sections 
    the steps section is an array , the final sections of the entities 
    the final obj is entities , it has 4 lists of the entite and its def
    
    """
    text=prompt.replace("text","video")
    #print(prompt)
    summary_dict={}
    sections=text.split("1. **")
    sections=sections[1].split("2. **")
    summary_dict["goal"]=sections[0]
    sections=sections[1].split("3. **")
    summary_dict["gloab_understanding"]=sections[0]
    sections=sections[1].split("4. **")
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
    splitted=[x.strip() for x in splitted if x.strip()!=""]
    return splitted[1:]

def prompt_2_json(prompt):
    """
    function contains break down of the info in the prompt , we have 4 sections 
    the steps section is an array , the final sections of the entities 
    the final obj is entities , it has 4 lists of the entite and its def
    
    """
    summary_dict=get_structures(prompt)
    summary_dict["steps"]=get_steps(summary_dict["steps"])
    summary_dict["entities"]=get_entities(summary_dict["entities"])
    