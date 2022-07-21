import ast
import sys

import requests
from pydantic import BaseModel

class Two(BaseModel):
    first: str
    second: str

class Command(BaseModel):
    method: str
    url: str
    data: list[Two]
        
def parse_commands(lines: list[str]) -> Command:
    method, url = lines.pop(0).split()

    twos = []
    for data in lines:
        if data:
            first, *second = data.split()
            twos.append(Two(first=first, second=''.join(second)))

    command = Command(method=method, url=url, data=twos)
    return command

def get_commands(filename: str) -> list[Command]:
    with open(filename) as f:
        xs = f.read().split('\n\n')
        ys = [ x.splitlines() for x in xs]
        commands = [ parse_commands(y) for y in ys ]
    return commands

if __name__ == "__main__":

    filename = sys.argv[1] if len(sys.argv) > 1 else 'api.http'
    commands = get_commands(filename=filename)
    errors = []

    for command in commands:
        if command.method == 'POST' and command.data[0].first == 'json':
            url = command.url
            json_data = ast.literal_eval(command.data[0].second)
            try:
                resp = requests.post(url, json=json_data)
                resp_data = resp.json()
                if resp.status_code == 200 and resp_data == ast.literal_eval(command.data[1].second):
                    print('.', end='')
                else:
                    msg = f'{command.method} - {command.url} failed'
                    # print(f'E {msg}')
                    print('E', end='')
                    errors.append(msg)
            except:
                msg = f'{command.method} - {command.url} failed'
                # print(f'E {msg}')
                print('E', end='')
                errors.append(msg)

            sys.stdout.flush()

    print('\n')
    for error in errors:
        print(error)
