import sys
import os
from collections import deque
import re
from colorama import Fore
import requests
from bs4 import BeautifulSoup


args = sys.argv
path = args[1]
if not os.access(path, os.F_OK):
    os.makedirs(path)
stack = deque()

while True:
    var = input()
    file_path = os.path.join(path, var)

    if os.access(file_path, os.F_OK):
        with open(file_path, 'r', encoding='utf-8') as file:
            print(file.read())
    else:
        if var == 'exit':
            sys.exit()
        elif var == 'back':
            if len(stack) > 1:
                stack.pop()
                print(stack.pop())
            continue

        url = var
        if not var.startswith('https://'):
            url = 'https://' + var
        try:
            response = requests.get(url)
            if response.status_code == requests.codes.OK:
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all("a"):
                    link.string = "".join([Fore.BLUE, link.get_text(), Fore.RESET])
                file_path = os.path.join(path, re.sub(r'\..+$', '', var))
                with open(file_path, 'w', encoding='utf-8') as file:
                    print(file_path)
                    print(soup.get_text(), file=file)
                    print(soup.get_text())
                    stack.append(soup.get_text())
            else:
                print("Incorrect URL")
        except requests.exceptions.ConnectionError:
            print("Incorrect URL")
