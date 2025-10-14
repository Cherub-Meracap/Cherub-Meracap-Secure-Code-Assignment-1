import os
import pymysql
import shlex
import subprocess
import requests
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv('db_config.env')

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    quote_body = shlex.quote(body)
    quote_subject = shlex.quote(subject)
    quote_to = shlex.quote(to)
    subprocess.run(f"printf '%s' {quote_body} | mail -s {quote_subject} {quote_to}"
                   , shell=True, check=True)

def get_data():
    url = 'https://secure-api.com/get-data'
    try:
        if not url.lower().startswith('https://'):
            raise ValueError("URL must start with HTTPS")
    
        response = requests.get(url, verify=True)
        response.raise_for_status()
        return response.text
    
    except requests.exceptions.SSLError as e:
        print(f"HTTPS for {url} is invalid: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred in request: {e}")
    except ValueError as e:
        print(f"Error: {e}")

def save_to_db(data):
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query, (data, 'Another Value'))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
