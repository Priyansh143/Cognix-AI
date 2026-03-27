from typing import List
import re
from autogen_core.models import SystemMessage
import ast
import asyncio

async def extract_jd_priorities_llm(jd_text: str, jd_role: str, max_topics: int, llm_call, logger = None) -> List[str]:
    """
    Uses an LLM to extract ordered JD priorities.
    `llm_call` should be a function that takes (system_prompt, user_prompt)
    and returns raw text.
    """
    MAX_RETRIES = 3
    user_prompt = f"""
        Extract the most important interview topics from the job role and job description.
        job role: {jd_role}
        Job Description:
        {jd_text}

        Return a Python list of dictionaries.

        Each dictionary must contain:
        - topic:a 2–4 word interview topic
        - keywords: 4–5 concise resume keywords related to that topic

        Rules:
        - Give ATMOST {max_topics} topics
        - topic must be 2–4 words
        - keywords must be concise resume terms
        - STRICTLY NO explanations
        - STRICTLY NO trailing text, only the list
        Example of output structure-
        [
        {{
        "topic": "model deployment",
        "keywords": ["deployed","model serving","fastapi","docker","production pipeline"]
        }},
        {{
        "topic": "feature engineering",
        "keywords": ["feature engineering","feature selection","feature extraction","data preprocessing","feature transformation"]
        }}
        ]
    """
    for attempt in range(MAX_RETRIES):

        try:
            response = await llm_call.create(
                messages=[SystemMessage(content=user_prompt)]
            )

            raw_output = response.content.strip()
            if logger:
                logger.info(f"Attempt {attempt+1} LLM output: {raw_output}")

            # extract list
            match = re.search(r"\[.*\]", raw_output, re.S)
            if not match:
                raise ValueError("No list found in LLM output")

            list_str = match.group(0)

            # parse safely
            try:
                topic_objects = json.loads(list_str)
            except:
                import ast
                topic_objects = ast.literal_eval(list_str)

            # validate
            if not isinstance(topic_objects, list):
                raise ValueError("Parsed output is not a list")

            cleaned = []
            for item in topic_objects:
                if isinstance(item, dict) and "topic" in item:
                    cleaned.append({
                        "topic": item.get("topic", "unknown"),
                        "keywords": item.get("keywords", [])
                    })

            if not cleaned:
                raise ValueError("No valid topics found")

            # limit
            cleaned = cleaned[:max_topics]
            topics = [item["topic"] for item in cleaned]

            return topics, cleaned

        except Exception as e:
            if logger:
                logger.warning(f"Attempt {attempt+1} failed: {e}")

    # ---- fallback ----
    if logger:
        logger.error("LLM failed after retries. Using fallback.")

    return (
        ["general discussion"],
        [{
            "topic": "general discussion",
            "keywords": ["experience", "projects", "skills"]
        }]
    )

def extract_jd_priorities_stub(
    job_role: str,
    job_description: str
) -> List[str]:
    return [
        "machine learning fundamentals",
        "model deployment",
        "data preprocessing",
        "model evaluation",
        "sql analytics"
    ]
    
