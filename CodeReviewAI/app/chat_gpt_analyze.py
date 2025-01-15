import openai
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
import asyncio

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_APIKEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")



async def analyze_code(assignment_description: str, files: Dict[str, str], candidate_level: str) -> Dict[str, Any]:
        """
        Analyze code quality using OpenAI GPT-4 Turbo.

        :param assignment_description: Project description
        :param files: Dictionary with filenames as keys and code as values
        :param candidate_level: Candidate level (Junior, Middle, Senior)
        :return: Dictionary containing the review
        """
        try:
            files_summary = "\n\n".join([f"### {filename}\n{content}" for filename, content in files.items()])

            prompt = f"""
You are a highly skilled and detail-oriented code reviewer with expertise in evaluating code quality, readability, and maintainability.
Your goal is to provide a professional review of the following code written by a {candidate_level} developer, considering their experience level.

**Project Description:**
{assignment_description}

**Code to Review:**
{files_summary}

### Instructions for Review:
1. **Analyze Each File:** Evaluate the provided code on a file-by-file basis. For each file, provide:
   - A brief summary of the file's purpose and functionality.
   - Strengths and positive aspects of the implementation.
   - Downsides or areas for improvement, with specific examples.
   
2. **General Feedback:** After analyzing individual files, offer a holistic view of the codebase. Discuss:
   - Overall code quality and adherence to industry best practices.
   - Readability and maintainability of the codebase.
   - Identification of any bugs, inefficiencies, or potential issues.
   - Suggestions for improving the project as a whole.

3. **Rating:** Provide a final rating of the code on a scale from 1 to 10, considering the developer's level.

4. **Conclusion:** Summarize your thoughts in 2-3 sentences, highlighting the key takeaways.

### Example Output Structure:
**File Analysis:**
- **File 1 (filename1.py):**
  - Purpose: [Brief description]
  - Strengths: [Strengths]
  - Downsides: [Weaknesses]
- **File 2 (filename2.js):**
  - Purpose: [Brief description]
  - Strengths: [Strengths]
  - Downsides: [Weaknesses]

**General Feedback:**
- Overall Quality: [Comments]
- Best Practices: [Adherence or lack thereof]
- Readability: [Comments]
- Issues Identified: [Summary of bugs/issues]

**Rating:** [Numeric score out of 10]

**Conclusion:** [2-3 sentence summary]

Please ensure your review is clear, actionable, and tailored to the developer's experience level.
"""


            response = await client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that reviews Python code for quality and correctness."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=3000,
            )

            return response.choices[0].message.content
        
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.

        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")

        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
            
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return {"error": "An unexpected error occurred."}
