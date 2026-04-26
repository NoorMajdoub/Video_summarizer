"""
prompts.py
All LLM prompt templates for the Video Summarizer.
"""


def get_summary_prompt(transcript: str) -> str:
    """
    Builds the prompt for generating a structured textual summary.
    Args:
        transcript: Plain text transcript of the video.
    Returns:
        Formatted prompt string ready to send to Gemini.
    """
    return f"""
You are an expert technical summarizer and knowledge graph builder.

Given the following video transcript:

"{transcript}"

Do the following:

1. **Goal**: Clearly state the main objective or purpose of the video in 1-2 sentences.

2. **Global Understanding**: Summarize the high-level idea of what is being explained or taught, in 2-4 sentences.

3. **Steps (if any)**: If the video contains steps, procedures, or sequential logic, list them clearly in order. Use bullet points and separate them with - for each step.

4. **Entity Extraction**:
  - Identify all unique entities or concepts mentioned in the video.
  - Organize them into the following categories:
    - People: list them and present the role of each
    - Tools / Libraries / Technologies: list them and present what they were used for
  - Present them as bullet points starting with -- for each entity.
"""


def get_visual_prompt(transcript: str) -> str:
    """
    Builds the prompt for generating entities and relations for the knowledge graph.
    Args:
        transcript: Plain text transcript of the video.
    Returns:
        Formatted prompt string ready to send to Gemini.
    """
    return f"""
You are an expert technical summarizer and knowledge graph builder.

Given the following video transcript:

{transcript}

Perform the following tasks with clear and structured output:

1. **Entities**
List all the key entities mentioned in the transcript. Present them as a bullet list.
Include entity types where possible (e.g., Person, Organization, Technology, etc.).

2. **Relations**
Identify and describe the relationships between the entities.
Present them as triples in the format:
**[Entity 1]—[Relation]—[Entity 2]**

Ensure the output is clean, easy to read, and grouped under clear section headers.
"""