from .github_client import fetch_github_issues
from .llm_factory import create_issue_analyzer


def analyze_github_issues(repo_name, github_token, model_name=None, post_comments=False, max_issues=10, state="open"):

    issues = fetch_github_issues(repo_name, github_token, state=state)[:max_issues]
    issue_analyzer = create_issue_analyzer(model_name=model_name)
    results = []
    for issue in issues:
        print(f"Analyzing Issue #{issue.number}: {issue.title}")

        body = issue.body if issue.body else "No description provided."

        suggestion = issue_analyzer.run(
            title=issue.title,
            body=body,
            repo_name=repo_name,
        )

        results.append({"issue_number": issue.number, "issue_title": issue.title, "suggestion": suggestion})

        if post_comments:
            comment = f"## 🤖 AI Issue Analysis\n\n{suggestion.strip()}\n\n---\n*This is an automated suggestion. Please consider its accuracy in context.*"
            issue.create_comment(comment)
            print(f"Posted comment on Issue #{issue.number}")
        else:
            print(f"Suggestion: {suggestion.strip()}\n")
    return results

