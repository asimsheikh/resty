import ast
import re
import sys
from typing import Literal, Any

import requests
from pydantic import BaseModel

class PostCommand(BaseModel):
    method: Literal['POST']
    url: str
    json_data: dict[Any, Any] | None
    equals: dict[Any, Any] | None

dict_pattern = r'\{.*?\}'
json_pattern = r'json ' + dict_pattern
equals_pattern = r'equals ' + dict_pattern
post_pattern_uppercase = r'\bPOST.+'
post_pattern = r'\b(post.+)'

def get_post_command(text_command: str) -> PostCommand:
    post_command = re.findall(post_pattern, text_command) or re.findall(post_pattern_uppercase, text_command)
    post_url = post_command[0].split('POST')[1].strip()
    
    json_command = re.findall(json_pattern, text_command, flags=re.DOTALL)
    json_dict = json_command[0].replace('json', '')
    json_dict = ast.literal_eval(json_dict.replace('\n', '').strip())
    
    equals_command = re.findall(equals_pattern, text_command, flags=re.DOTALL)
    equals_dict = equals_command[0].replace('equals', '')
    equals_dict = ast.literal_eval(equals_dict.replace('\n', '').strip())
    
    return PostCommand(method='POST', url=post_url, json_data=json_dict, equals=equals_dict)

def extract_commnds(httpfile: str) -> list[str]:
    pattern = r'\n{2}'
    xs = re.finditer(pattern, httpfile)
    ys = [0] + [ x.span()[1] for x in xs ]
    zs = list(zip(ys, ys[1:]))
    ps = [ httpfile[x:y] for x,y in zs ]
    return ps

def runner(commands: list[str]) -> None:
    for command in commands:
        req = get_post_command(command)
        print(req)
        print(requests.post(req.url, json=req.json_data).json())

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'api.http'
    with open(filename) as fn:
        httpfile = fn.read()
   
    commands = extract_commnds(httpfile)
    runner(commands) 



