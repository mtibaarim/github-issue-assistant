import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from issue_assistant.llm_factory import create_issue_analyzer
from github import Github
from dotenv import load_dotenv
import json


def main():
    load_dotenv()

    github_token = os.environ["GITHUB_TOKEN"]      
    event_path = os.environ["GITHUB_EVENT_PATH"]   

    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)

    repo_full_name = event["repository"]["full_name"]  
    issue_number = event["issue"]["number"]

    print(f"🔧 Repo: {repo_full_name}, issue #{issue_number}")

    gh = Github(github_token)
    repo = gh.get_repo(repo_full_name)
    issue = repo.get_issue(number=issue_number)

    analyzer = create_issue_analyzer(
        model_name="llama-3.3-70b-versatile",
        temperature=0.0,
    )


    suggestion = analyzer.run(
        title=issue.title,
        body=issue.body ,
        repo_name=repo_full_name,
    ).strip()

    comment = (
        "## AI Issue Analysis\n\n"
        f"{suggestion}\n\n"
        "---\n"
        "*This is an automated suggestion. Please consider its accuracy in context.*"
    )

    issue.create_comment(comment)
    print(f"✅ Posted AI comment on issue #{issue.number}")

if __name__ == "__main__":
    main()
