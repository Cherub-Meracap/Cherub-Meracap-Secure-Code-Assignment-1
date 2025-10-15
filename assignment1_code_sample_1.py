import os
import pymysql
import subprocess
import requests
import re
from dotenv import load_dotenv

load_dotenv('db_config.env')

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_user_input():
    try:
        user_input = input('Enter your name: ').strip().lower()
        if user_input == '':
            raise ValueError("Input cannot be empty")
        if not re.match(r"^[a-zA-Z0-9_-]+$", user_input):
            raise ValueError("User name is invalid")
        return user_input
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None

def send_email(to, subject, body):
    try:
        if not re.match(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", to, re.IGNORECASE):
            raise ValueError("Invalid email address")
        if "\n" in subject or "\r" in subject:
            raise ValueError("Invalid characters in subject")
        subprocess.run(['mail', '-s', subject, to], input=body.encode(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error sending email: {e}")
    except ValueError as e:
        print(f"Error: {e}")

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
