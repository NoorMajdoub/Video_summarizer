"""
prompt2dict.py
Parses the raw LLM textual summary output into a structured Python dictionary.
"""


def get_structures(prompt):
    """
    Pase the LLM output to extract the sections we need and save them in a dictionnary
    Args:
        Prompt: str : the output of the model
    Returns : 
        summary_dict : dict : the clean sections of the LLM 
    """
    import re

    summary_dict = {}

    goal_match = re.search(r'GOAL:\s*(.*?)(?=GLOBAL UNDERSTANDING:)', prompt, re.DOTALL)
    summary_dict["goal"] = goal_match.group(1).strip() if goal_match else ""

    global_match = re.search(r'GLOBAL UNDERSTANDING:\s*(.*?)(?=STEPS:)', prompt, re.DOTALL)
    summary_dict["global_understanding"] = global_match.group(1).strip() if global_match else ""

    steps_match = re.search(r'STEPS:\s*(.*?)(?=ENTITY EXTRACTION:)', prompt, re.DOTALL)
    if steps_match:
        # Match any "- something" bullet, not just "- Step N:"
        summary_dict["steps"] = [
            s.strip() for s in re.findall(r'-\s*(.+)', steps_match.group(1))
            if s.strip()
        ]
    else:
        summary_dict["steps"] = []

    entities_match = re.search(r'ENTITY EXTRACTION:\s*(.*?)$', prompt, re.DOTALL)
    if entities_match:
        # Match "Name: description" lines (with or without leading dash)
        summary_dict["entities"] = re.findall(r'-?\s*([\w\s/,]+?):\s*([^\n]+)', entities_match.group(1))
        summary_dict["entities"] = [
            [name.strip(), desc.strip()] 
            for name, desc in summary_dict["entities"]
            if name.strip() and desc.strip()
        ]
    else:
        summary_dict["entities"] = []

    return summary_dict



def prompt_2_json(prompt: str) -> dict:
    summary_dict = get_structures(prompt)
    # get_structures now returns steps and entities already parsed
    # so get_steps and get_entities are no longer needed
    return summary_dict

def prompt_2_json(prompt):
    summary_dict = get_structures(prompt)
    # get_structures now returns steps and entities already parsed
    # so get_steps and get_entities are no longer needed
    return summary_dict
