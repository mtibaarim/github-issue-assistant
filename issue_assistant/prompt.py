"""Prompt template for issue analysis.

This file is defensive about importing `PromptTemplate` because
LangChain has moved modules between releases. We try common import
locations and fall back to a tiny local shim so the rest of the
project can run even if LangChain's API differs.
"""

try:
    from langchain.prompts import PromptTemplate
except Exception:
    try:
        from langchain.prompts.prompt import PromptTemplate
    except Exception:
        class PromptTemplate:
            def __init__(self, *, input_variables, template):
                self.input_variables = input_variables
                self.template = template

            def format(self, **kwargs):
                # Basic Python str.format-based rendering
                return self.template.format(**kwargs)


issue_prompt = PromptTemplate(
    input_variables=["title", "body", "repo_name"],
    template="""
    You are an experienced software engineer helping triage GitHub issues.

    REPOSITORY: {repo_name}
    ISSUE TITLE: {title}
    ISSUE DESCRIPTION: {body}

    Based on the issue description above:
    1) Identify the most likely root cause of the problem
    2) Suggest a specific approach to fix it
    3) If relevant, mention any files or components that might need changing

    FORMAT YOUR RESPONSE IN MARKDOWN WITH SECTIONS:
    - Likely Cause
    - Suggested Fix
    - Relevant Components

    Keep your response concise (max 200 words) but technically precise.
    If you can't determine the cause from the information provided, suggest what additional information would help.
    """,
)