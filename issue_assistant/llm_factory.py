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
        # Build the prompt text using your PromptTemplate
        try:
            # Standard PromptTemplate API
            prompt_text = issue_prompt.format(**inputs)
        except Exception:
            # Fallback: last resort – just stringify inputs
            prompt_text = str(inputs)

        # Call Groq via LangChain
        response = self.llm.invoke(prompt_text)

        # ChatGroq returns an AIMessage; take the content
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

# import os
# try:
#     from langchain.chains import LLMChain
# except Exception:
#     try:
#         from langchain.chains.llm import LLMChain
#     except Exception:
#         LLMChain = None

# try:
#     from langchain_groq import GroqChat as _GroqChat
# except Exception:
#     try:
#         from langchain_groq import ChatGroq as _GroqChat
#     except Exception:
#         _GroqChat = None

# from .prompt import issue_prompt

# def create_issue_analyzer(model_name="llama-3.3-70b-versatile", temperature=0):
#     """
#     Create an LLM chain for analyzing GitHub issues using Groq Llama 3.3 70B.

#     Args:
#         model_name (str): Groq model to use (default llama-3.3-70b-versatile)
#         temperature (float): Creativity level (0-1)
        
#     Returns:
#         LLMChain: Configured LLM chain
#     """
    
#     if LLMChain is not None and _GroqChat is not None:
#         llm = _GroqChat(
#             model_name=model_name,
#             temperature=temperature,
#             groq_api_key=os.getenv("GROQ_API_KEY"),
#         )

#         return LLMChain(llm=llm, prompt=issue_prompt)

#     try:
#         from groq import Groq
#     except Exception as e:
#         raise RuntimeError(
#             "Neither LangChain LLMChain nor groq client are available.\n"
#             "Install `langchain` or `groq` (and optionally `langchain-groq`)."
#         ) from e

#     groq_api_key = os.getenv("GROQ_API_KEY")
#     if not groq_api_key:
#         raise RuntimeError("GROQ_API_KEY environment variable is not set")

#     groq_client = Groq(api_key=groq_api_key)

#     class GroqIssueAnalyzer:
#         def __init__(self, client, model, temperature):
#             self.client = client
#             self.model = model
#             self.temperature = temperature

#         def run(self, inputs: dict) -> str:
#             if hasattr(issue_prompt, 'format'):
#                 prompt_text = issue_prompt.format(**inputs)
#             else:
#                 try:
#                     prompt_text = issue_prompt.template.format(**inputs)
#                 except Exception:
#                     prompt_text = str(inputs)

#             response = self.client.chat.completions.create(
#                 model=model_name,
#                 messages=[{"role": "user", "content": prompt_text}],
#                 max_tokens=512,
#             )

#             try:
#                 return response.choices[0].message.content
#             except Exception:
#                 return getattr(response, 'text', str(response))

#     return GroqIssueAnalyzer(groq_client, model_name, temperature)


