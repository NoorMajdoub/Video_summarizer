"""
prompt2dict.py
Parses the raw LLM textual summary output into a structured Python dictionary.
"""


def get_structures(prompt):
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


def get_steps(steps):   #unused
    split = steps.split("-")
    if len(split) < 2:
        return ["This video contains no clear steps."]
    
    cleaned = []
    for s in split:
        s = s.replace("*", "").replace("\n", " ").strip()
        # Remove leading numbers and dots like "1." "2." etc
        s = re.sub(r"^\d+[\.\)]\s*", "", s)
        # Remove leftover section headers
        if any(skip in s for skip in ["if any", "Steps", "Entity", "4."]):
            continue
        if s:
            cleaned.append(s)
    
    return cleaned

def get_entities(entities):
    """
    Parses the entities section string into a list of [name, description] pairs.
    Args:
        entities: Raw entities section string from Gemini output.
    Returns:
        List of [entity_name, description] pairs.
    """
    split = entities.split("--")
    split = [x for x in split if x.strip()]
    split = [
        x.replace("*", "").replace(",", "").replace("\n", "").strip()
        for x in split
    ]

    result = []
    for item in split:
        parts = item.split(":", 1)  # split on first colon only
        if len(parts) == 2 and parts[0].strip() and parts[1].strip():
            result.append([parts[0].strip(), parts[1].strip()])

    return result

def prompt_2_json(prompt):
    summary_dict = get_structures(prompt)
    # get_structures now returns steps and entities already parsed
    # so get_steps and get_entities are no longer needed
    return summary_dict
