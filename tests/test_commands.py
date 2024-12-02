from app.commands.commands import create_user, seed_data


def test_create_user(runner):
    result = runner.invoke(create_user, ["--username", "TestUser1", "--password", "TestUser1", "--role", "user"])

    assert result.exit_code == 0
    assert result.output


def test_seed_data(runner):
    result = runner.invoke(seed_data)

    assert result.exit_code == 0
    assert result.output