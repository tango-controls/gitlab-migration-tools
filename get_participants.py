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

# prompt for options
owner = input(f"Repo owner [{owner}] ? ", ) or owner
repo = input(f"Repo name [{repo}] ? ") or repo
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
    print(f"getting commenters (page({p}): {len(r)}")
    if len(r) < per_page:
        break

# report unique names
unique_users = [f"@{u}" for u in sorted(set(commenters + contributors))
                if u not in excluded_users]
print(f"\nUnique users for github.com/{owner}/{repo}:")
print(", ".join(unique_users))
