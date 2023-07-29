import os
from agentshell.main import (
    get_files_in_cwd,
    get_current_shell,
    set_current_shell,
    set_cwd,
    get_history,
    get_history_formatted,
    add_to_shell_history,
    clear_history,
    wipe_all,
    list_active_shells,
    close_shell,
    new_shell,
    get_cwd,
    run_command,
)


def setup():
    # Creating a new shell for tests
    shell_id = new_shell()
    set_current_shell(shell_id)
    return shell_id


def teardown(shell_id):
    if not isinstance(shell_id, (str, int)):
        return
    # Closing the shell after tests
    close_shell(shell_id)


def test_run_command():
    shell_id = setup()
    command = "echo Hello, World!"
    result = run_command(command, shell_id)

    # The command should run successfully
    assert result["success"] == True
    teardown(shell_id)


def test_get_cwd():
    shell_id = setup()

    # set_cwd and then get_cwd to check if the directory was set correctly
    set_cwd("/tmp", shell_id)
    result = get_cwd(shell_id)

    assert result == "/tmp"
    teardown(shell_id)


def test_get_history_formatted():
    shell_id = setup()
    run_command("echo Hello, World!", shell_id)
    history = get_history_formatted(shell_id)

    # Assert that the history contains the command we just ran
    assert "echo Hello, World!" in history

    teardown(shell_id)


def test_get_files_in_cwd():
    shell_id = setup()

    basename = os.path.basename(__file__)

    # Change to a known directory and check the files
    set_cwd(os.path.dirname(os.path.abspath(__file__)), shell_id)
    files = get_files_in_cwd(shell_id)

    # Assert that the known file is in the list of files
    assert os.path.basename(basename) in "\n".join(files)

    teardown(shell_id)


def test_get_current_shell():
    # Create a new shell
    shell_id = new_shell()
    # Set it as the current shell
    set_current_shell(shell_id)

    # Check if the current shell is the one we just created
    assert get_current_shell() == shell_id

    # Clean up
    teardown(shell_id)


def test_add_to_shell_history():
    shell_id = setup()

    # Add a command to the history
    add_to_shell_history(shell_id, "ls -la", True, "command output", "")

    # Check if the command appears in the shell's history
    history = get_history(shell_id)
    assert any(item["metadata"]["command"] == "ls -la" for item in history)

    # Clean up
    teardown(shell_id)


def test_clear_history():
    shell_id = setup()

    # Add a command to the history
    add_to_shell_history(shell_id, "ls -la", True, "command output", "")

    # Clear the shell's history
    clear_history(shell_id)

    # Check if the history is indeed empty
    history = get_history(shell_id)
    assert len(history) == 0

    # Clean up
    teardown(shell_id)


def test_wipe_all():
    setup()
    # Create a new shell
    shell_id = new_shell()
    # Add it to the history
    add_to_shell_history(shell_id, "ls -la", True, "command output", "")
    # Clear all shells and histories
    wipe_all()

    # Check if all shells and histories have been wiped
    assert len(list_active_shells()) == 0
    assert len(get_history(shell_id)) == 0
    teardown(shell_id)


def test_list_active_shells():
    # Create new shells
    shell_id1 = new_shell()
    shell_id2 = new_shell()

    # Check if both shells appear in the list of active shells
    active_shells = list_active_shells()
    assert shell_id1 in active_shells
    assert shell_id2 in active_shells

    # Clean up
    close_shell(shell_id1)
    close_shell(shell_id2)


def test_close_shell():
    # Create a new shell
    shell_id = new_shell()

    # Close the shell
    close_shell(shell_id)

    # Check if the shell does not appear in the list of active shells
    active_shells = list_active_shells()
    assert shell_id not in active_shells

    # No need for teardown because close_shell() already deletes the shell


def test_new_shell():
    # Create a new shell
    shell_id = new_shell()

    # Check if the new shell appears in the list of active shells
    active_shells = list_active_shells()
    assert shell_id in active_shells

    # Clean up
    teardown(shell_id)
