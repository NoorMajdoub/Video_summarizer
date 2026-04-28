"""
prompts.py
All LLM prompt templates for the Video Summarizer.
"""
def get_code_cleaning_prompt(transcript: str) -> str:
    return f"""
You are an expert software engineer specializing in cleaning and reconstructing code from noisy OCR output.

You will be given text that contains code mixed with OCR errors, formatting issues, and irrelevant noise.

Your task is to:

1. Extract ONLY the code from the text.
2. Remove all non-code content (explanations, timestamps, captions, etc.).
3. Fix common OCR errors such as:
   - incorrect characters (e.g., 'l' vs '1', 'O' vs '0')
   - broken indentation
   - missing or incorrect symbols
   - split or merged lines
4. Reconstruct the code into a clean, readable, and executable format.
5. Preserve the original programming language.
6. If something is unclear, make the most reasonable assumption to fix it.
7. Do NOT explain anything.

Output ONLY the cleaned code , Without notes in before or after the code.

Input:
'{transcript}'  """



def get_summary_prompt(transcript: str) -> str:
            return f"""
        You are an expert technical summarizer and knowledge graph builder.
        Given the following video transcript:
        '{transcript}'
        
        Reply using EXACTLY this structure with EXACTLY these headers, do not change or rephrase them:
        
        GOAL:
        [1-2 sentences stating the main objective]
        
        GLOBAL UNDERSTANDING:
        [2-4 sentences summarizing the high-level idea]
        
        STEPS:
        - Step 1: [description]
        - Step 2: [description]
        - Step 3: [description]
        
        ENTITY EXTRACTION:
        - EntityName: [what it is / role]
        - EntityName: [what it is / role]
        
        Do not add numbered prefixes, markdown bold, or any extra formatting outside of what is shown above.
            """
