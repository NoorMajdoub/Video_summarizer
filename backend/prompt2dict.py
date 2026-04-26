"""
prompt2dict.py
Parses the raw Gemini textual summary output into a structured Python dictionary.
"""


def get_structures(prompt: str) -> dict:
    """
    Splits the raw Gemini response into its four sections:
    goal, global_understanding, steps, and entities.

    Args:
        prompt: Raw text response from Gemini.

    Returns:
        Dictionary with keys: goal, global_understanding, steps, entities (all raw strings).
    """
    # Normalize: replace "text" with "video" so the output feels video-specific
    text = prompt.replace("text", "video")

    summary_dict = {}

    sections = text.split("Goal")
    sections = sections[1].split("Global Understanding")
    summary_dict["goal"] = sections[0][2:-2].strip()

    sections = sections[1].split("Steps")
    summary_dict["global_understanding"] = (
        sections[0].replace("*", " ").replace("3", "").strip()
    )

    sections = sections[1].split("Entity Extraction")
    summary_dict["steps"] = sections[0]
    summary_dict["entities"] = sections[1]

    return summary_dict


def get_steps(steps: str) -> list:
    """
    Parses the steps section string into a list of step strings.

    Args:
        steps: Raw steps section string from Gemini output.

    Returns:
        List of step strings, or a fallback message if no steps found.
    """
    split = steps.split("-")
    if len(split) < 2:
        return ["This video contains no clear steps."]
    return [s.replace("*", " ").strip() for s in split if s.strip()]


def get_entities(entities: str) -> list:
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


def prompt_2_json(prompt: str) -> dict:
    """
    Converts the raw Gemini summary response into a structured dictionary.

    Args:
        prompt: Raw Gemini response string.

    Returns:
        Dictionary with keys:
            - goal (str)
            - global_understanding (str)
            - steps (list of str)
            - entities (list of [name, description] pairs)
    """
    summary_dict = get_structures(prompt)
    summary_dict["steps"] = get_steps(summary_dict["steps"])
    summary_dict["entities"] = get_entities(summary_dict["entities"])
    return summary_dict