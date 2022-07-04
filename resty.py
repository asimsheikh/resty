import ast

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
    twos = []
    for data in lines[1:]:
        if data:
            first, *second = data.split()
            twos.append(Two(first=first, second=''.join(second)))

    method, url = lines[0].split()
    command = Command(method=method, url=url, data=twos)
    return command

def get_commands() -> list[Command]:
    with open('api.http') as f:
        xs = f.read().split('\n\n')
        ys = [ x.splitlines() for x in xs]
        commands = [ parse_commands(y) for y in ys ]
    return commands

if __name__ == "__main__":
    commands = get_commands()
    for command in commands:
        if command.method == 'POST' and command.data[0].first == 'json':
            url = command.url
            json_data = ast.literal_eval(command.data[0].second)
            try:
                resp = requests.post(url, json=json_data)
                if resp.status_code == 200:
                    print('.', end='')
                else:
                    print('E', end='')
            except:
                print('E', end='')
    print()
