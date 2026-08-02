import requests
import streamlit as st

url = "https://api.clockify.me/api/v1/user"


def get_workspace_id(api_key, headers):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"Clockify API-Fehler ({response.status_code}): {response.text}")
        st.stop()

    user = response.json()

    workspace_id = user["activeWorkspace"]
    username = user["name"]
    # USER_ID = user["id"]
    # print(f"Name: {user['name']}")
    # print(f"Email: {user['email']}")
    # print(f"Active Workspace: {user['activeWorkspace']}")
    # print(f"Default Workspace: {user['defaultWorkspace']}")

    return workspace_id, username
