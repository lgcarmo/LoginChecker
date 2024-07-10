import requests
import re
import argparse
from bs4 import BeautifulSoup
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def show_banner():
    banner = """
#####################################################################
#  _                 _        _____ _               _             	#
# | |               (_)      / ____| |             | |            	#
# | |     ___   __ _ _ _ __ | |    | |__   ___  ___| | _____ _ __ 	#
# | |    / _ \ / _` | | '_ \| |    | '_ \ / _ \/ __| |/ / _ \ '__|	#
# | |___| (_) | (_| | | | | | |____| | | |  __/ (__|   <  __/ |   	#
# |______\___/ \__, |_|_| |_|\_____|_| |_|\___|\___|_|\_\___|_|   	#
#               __/ |                                             	#
#              |___/                                              	#
#####################################################################
    """
    print(banner)


def parse_args():
    parser = argparse.ArgumentParser(description='Automated login script.')
    parser.add_argument('-f', '--file', type=str, required=True, help='File containing list of URLs.')
    parser.add_argument('-u', '--username', type=str, required=True, help='Username for login.')
    parser.add_argument('-p', '--password', type=str, required=True, help='Password for login.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def get_login_form(url, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = session.get(url, headers=headers, verify=False, timeout=30)
        print(f"GET {url} - Status Code: {response.status_code}")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve URL {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    forms = soup.find_all('form')
    csrf_token = None

    for form in forms:
        user_field = None
        pass_field = None

        inputs = form.find_all('input')
        for input_field in inputs:
            if re.search(r'user|email|login|username|usuario', input_field.get('name', ''), re.IGNORECASE):
                user_field = input_field.get('name')
                print(f"Found username field: {user_field}")
            if re.search(r'pass|password|secretkey|senha', input_field.get('name', ''), re.IGNORECASE):
                pass_field = input_field.get('name')
                print(f"Found password field: {pass_field}")
            if input_field.get('name') in ['csrfmiddlewaretoken', 'csrf_token', 'ftm_push_enabled', 'token_code']:
                csrf_token = input_field.get('value')

        if user_field and pass_field:
            action = form.get('action')
            if not action or action == '#':
                action = url
            elif not action.startswith('http'):
                action = url.rstrip('/') + '/' + action.lstrip('/')
            print(f"Using form action URL: {action}")
            return action, user_field, pass_field, csrf_token

    return None


def attempt_login(url, login_url, username, password, user_field, pass_field, csrf_token, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': url
    }
    login_data = {user_field: username, pass_field: password}
    if csrf_token:
        login_data['csrf_token'] = csrf_token
    print(f"Payload for POST request: {login_data}")
    try:
        response = session.post(login_url, data=login_data, headers=headers, cookies=session.cookies, verify=False,
                                timeout=30)
        print(f"POST {login_url} - Status Code: {response.status_code}")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to login at {url}: {e}")
        if response.status_code:
            print(f"Status Code: {response.status_code}")
        return False

    if response.url != url:
        print(f"Redirected to {response.url}, login successful.")
        return True
    elif re.search(r'logout|dashboard|profile', response.text, re.IGNORECASE):
        print("Login successful based on page content.")
        return True
    print("Login failed.")
    return False


def main():
    show_banner()
    args = parse_args()

    with open(args.file, 'r') as f:
        urls = f.readlines()

    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    for url in urls:
        url = url.strip()
        print("=" * 60)
        print(f"Processing URL: {url}")
        print("=" * 60)
        login_form = get_login_form(url, session)
        if login_form:
            action, user_field, pass_field, csrf_token = login_form
            success = attempt_login(url, action, args.username, args.password, user_field, pass_field, csrf_token,
                                    session)
            if success:
                print(f"\033[92m[+] Successfully logged into {url}\033[0m\n")
            else:
                print(f"\033[91mFailed to log into {url}\033[0m\n")
        else:
            print(f"\033[91m[-] No login form found for {url}\033[0m\n")
        print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
