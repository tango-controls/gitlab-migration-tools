import requests

# default parameters
owner = "tango-controls"
repo = "pytango"
excluded_users = [
    "dependabot[bot]",
    "codecov[bot]",
    "tango-controls-bot",
    "sonarcloud[bot]",
    "codacy-badger",
]
per_page = 100
api_user = ""
api_user_token = ""

# prompt for options
owner = input(f"Repo owner [{owner}] ? ", ) or owner
repo = input(f"Repo name [{repo}] ? ") or repo
api_user = input(f"API user  (empty for unauthenticated access) [] ? ") or api_user
if api_user:
    import getpass
    print("see https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token")
    logged = ""
    while not logged:
        api_token = getpass.getpass(f"access token for {api_user} (not echoed)? ")
        r = requests.get('https://api.github.com/user', auth=(api_user, api_token))
        logged = r.json().get("login", "")
        if logged:
            print(f"logged as {logged}")
        else:
            print("\nAuthentication error\n")

# excluded_users = " ".join(excluded_users)
# excluded_users = (input(f"excluded users [{excluded_users}] ? ") or excluded_users).split()
print()

# extract user names from people that contributed commits
contributors = []
for p in range(1, 200):
    r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page={per_page};page={p}").json()
    contributors += [c["login"] for c in r]
    print(f"getting contributors (page {p}): {len(r)}")
    if len(r) < per_page:
        break

# extract user names from people that commented
commenters = []
for p in range(1, 200):
    r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues/comments?per_page={per_page};page={p}").json()
    commenters += [c["user"]["login"] for c in r]
    print(f"getting commenters (page {p}): {len(r)}")
    if len(r) < per_page:
        break

for p in range(1, 200):
    r = requests.get(f"https://api.github.com/repos/{owner}/{repo}/pulls/comments?per_page={per_page};page={p}").json()
    commenters += [c["user"]["login"] for c in r]
    print(f"getting pr commenters (page {p}): {len(r)}")
    if len(r) < per_page:
        break

# report unique names
unique_users = [f"@{u}" for u in sorted(set(commenters + contributors))
                if u not in excluded_users]
print(f"\nUnique users ({len(unique_users)}) for github.com/{owner}/{repo}:")
print(", ".join(unique_users))
