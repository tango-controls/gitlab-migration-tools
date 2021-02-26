import requests

# default parameters
owner = "tango-controls"
repo = "pytango"
exclude_file = "./excluded"

per_page = 100
api_user = ""
api_user_token = ""

# prompt for options
owner = input(f"Repo owner [{owner}] ? ", ) or owner
repo = input(f"Repo name [{repo}] ? ") or repo
exclude_file = input(f"File with excluded accounts [{exclude_file}] ? ") or exclude_file

exclude_list = []
with open(exclude_file) as f:
    for line in f:
        if line.strip().startswith("#"):
            continue
        exclude_list += line.split()

# Exclude users registered in https://mensuel.framapad.org/p/migration_ready_2548763689
r = requests.get("https://mensuel.framapad.org/p/migration_ready_2548763689/export/txt")
registered_users = [
    line.strip().split()[0]
    for line in r.text.split("\n")
    if line.strip() and (not line.strip().startswith("#"))
]
exclude_list.extend(registered_users)

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
                if u not in exclude_list]

excluded_users = [f"@{u}" for u in sorted(set(commenters + contributors))
                if u in exclude_list]

print(f"\nUnique users ({len(unique_users)}) for github.com/{owner}/{repo}:")
print(", ".join(unique_users))

print(f"\nExcluded users ({len(excluded_users)}) for github.com/{owner}/{repo}:")
print(", ".join(excluded_users))
