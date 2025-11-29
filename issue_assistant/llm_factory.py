import os
from langchain_groq import ChatGroq

from .prompt import issue_prompt


class IssueAnalyzer:
    """
    Simple wrapper so the rest of the project can call:

        analyzer = create_issue_analyzer(...)
        suggestion = analyzer.run(
            title=...,
            body=...,
            repo_name=...,
        )

    This avoids depending on LLMChain / langchain.chains, which
    are unstable across LangChain versions.
    """

    def __init__(self, llm):
        self.llm = llm

    def run(self, **inputs) -> str:
        """
        Runs the analysis. Accepts keyword args like:
            run(title="...", body="...", repo_name="...")
        """
        try:
            prompt_text = issue_prompt.format(**inputs)
        except Exception:
            prompt_text = str(inputs)

        response = self.llm.invoke(prompt_text)

        return getattr(response, "content", str(response))


def create_issue_analyzer(
    model_name: str = "llama-3.3-70b-versatile",
    temperature: float = 0.0,
) -> IssueAnalyzer:
    """
    Create an analyzer for GitHub issues using Groq Llama 3.3 70B.

    Returns an IssueAnalyzer object with a .run(**kwargs) method.
    """

    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set")

    llm = ChatGroq(
        model_name=model_name,
        temperature=temperature,
        groq_api_key=groq_api_key,
    )

    return IssueAnalyzer(llm)