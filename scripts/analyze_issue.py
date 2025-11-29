import json
import os

from github import Github
from issue_assistant.llm_factory import create_issue_analyzer
from dotenv import load_dotenv

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

    body = issue.body or "[No description provided]"

    suggestion = analyzer.run(
        title=issue.title,
        body=body,
        repo_name=repo_full_name,
    ).strip()

    comment = (
        "## 🤖 AI Issue Analysis\n\n"
        f"{suggestion}\n\n"
        "---\n"
        "*This is an automated suggestion. Please consider its accuracy in context.*"
    )

    issue.create_comment(comment)
    print(f"✅ Posted AI comment on issue #{issue.number}")

if __name__ == "__main__":
    main()
