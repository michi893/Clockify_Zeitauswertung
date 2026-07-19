import requests

url = "https://api.clockify.me/api/v1/user"

def get_workspace_id(API_KEY, headers):
    # Get user information
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user = response.json()
        USER_ID = user['id']
        WORKSPACE_ID = user['activeWorkspace']
        #print(f"Name: {user['name']}")
        #print(f"Email: {user['email']}")
        #print(f"Active Workspace: {user['activeWorkspace']}")
        #print(f"Default Workspace: {user['defaultWorkspace']}")
    return WORKSPACE_ID, USER_ID