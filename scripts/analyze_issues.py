from dotenv import load_dotenv
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from issue_assistant.analyzer import analyze_github_issues
import os


def main():
    load_dotenv()

    repo_name = os.getenv("REPO_NAME")
    github_token = os.getenv("GITHUB_TOKEN")

    if not repo_name:
        raise RuntimeError("REPO_NAME is missing in .env")
    if not github_token:
        raise RuntimeError("GITHUB_TOKEN is missing in .env")

    print(f"Analyzing issues for repo: {repo_name}")

    suggestions = analyze_github_issues(
        repo_name=repo_name,
        github_token=github_token,
        model_name="llama-3.3-70b-versatile",
        post_comments=False,
        max_issues=2,
    )

    for item in suggestions:
        print("\n" + "=" * 80)
        print(f"Issue #{item['issue_number']}: {item['issue_title']}")
        print(item["suggestion"])

if __name__ == "__main__":
    main()
