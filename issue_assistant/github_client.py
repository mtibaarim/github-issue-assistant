from github import Github, Auth

def fetch_github_issues(repo_name, token=None, state='open'):
    '''
    Fetch issues from a GitHub repository.
    Args:
        repo_name (str): The full name of the repository ('owner/repo').
        token (str, optional): GitHub personal access token for authentication.
        state (str, optional): The state of the issues to fetch ('open', 'closed', 'all').
    Returns:
        list: A list of issues from the repository.
    '''

    if token:
        g = Github(auth=Auth.Token(token))
    else:
        g = Github()

    repo = g.get_repo(repo_name)
    issues = list(repo.get_issues(state=state))

    print(f"Found {len(issues)} {state} issues in {repo_name}")

    return issues

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")
    issues = fetch_github_issues("langchain-ai/langchain", github_token)
    for issue in issues[:3]:  
        print(f"#{issue.number}: {issue.title}")