from urllib.error import HTTPError
from urllib.request import urlopen
from dataclasses import dataclass

@dataclass
class Command:
    method: str
    address: str

def parse_command(text: str) -> Command: 
    method, address = text.split()
    return Command(method=method, address=address)

def run_command(command: Command) -> dict[str, bool]:
    try:
        with urlopen(command.address) as response:
            if response.status == 200:
                return {'ok': True}
            else:
                return {'ok': False}
    except HTTPError:
            return {'ok': False}
