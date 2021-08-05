import requests
import secrets
import json
import api_utils

CLIENT_ID = ""
CLIENT_SECRET = ""
ACCESS_TOKEN = ""

def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

def print_auth_url(code_challenge: str):
    global CLIENT_ID

    url = f"https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}"
    print("Authorization link:\n" + url)

def generate_new_token(auth_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': auth_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()

    token = response.json()
    response.close()
    print("Token successfully generated.")

    with open('token.json', 'w') as f:
        json.dump(token, f, indent=4)
        print('Token saved in "token.json"')

    return token

def get_auth_code() -> str:
    auth_code = input('Copy-paste the localhost link: ').strip()
    auth_code = auth_code.replace("http://localhost/oauth?code=", '')
    print(f'Your Authentication Code is:\n{auth_code}')
    return auth_code

def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")

if __name__ == "__main__":
    CLIENT_ID = input("Please enter your CLIENT_ID: ").strip()
    CLIENT_SECRET = input("Please enter your CLIENT_SECRET: ").strip()

    code_verifier = code_challenge = get_new_code_verifier()
    print_auth_url(code_challenge)
    auth_code = get_auth_code()

    token = generate_new_token(auth_code, code_verifier)
    ACCESS_TOKEN = token['access_token']
    print_user_info(ACCESS_TOKEN)

    fields = [
        'id',
        'title',
        'alternative_titles',
        'start_date',
        'synopsis',
        'mean',
        'rank',
        'average_episode_duration',
        'genres',
        'num_episodes',
        'studios',
        "nsfw"
    ]

    api_utils.generate_df(ACCESS_TOKEN, 6, fields)