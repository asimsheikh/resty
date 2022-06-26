from resty import parse_command, Command, run_command

def test_parse_command():
    text = "GET http://localhost:5000/hello"
    assert parse_command(text) == Command(method='GET',
            address="http://localhost:5000/hello")

    text = "GET http://localhost:5000/people"
    assert parse_command(text) == Command(method='GET',
            address="http://localhost:5000/people")

def test_run_command():
    text = "GET http://localhost:5000/hello"
    command = parse_command(text)
    assert run_command(command) == {'ok': True}

    text = "GET http://localhost:5000/people"
    command = parse_command(text)
    assert run_command(command) == {'ok': False}
