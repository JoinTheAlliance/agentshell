import subprocess
import os
import time
from agentmemory import (
    create_memory,
    delete_memories,
    delete_memory,
    get_memories,
    get_memory,
    update_memory,
    wipe_category,
)


def get_files_in_cwd(shell_id=None):
    """
    Returns a list of files in the current directory of a specific shell.

    Parameters:
    shell_id (str): The unique identifier of the shell. If not specified, uses the current shell.

    Returns:
    list: A list of filenames in the current directory.
    """

    if shell_id is None:
        shell_id = get_current_shell()
    shell = get_memory("shell", shell_id)
    cwd = shell["metadata"]["cwd"]

    # call ls -alh in the current working directory
    result = subprocess.check_output(f"ls -alh {cwd}", shell=True)
    result_decoded = result.decode("utf-8").strip().split("\n")
    # remove the first line, which is the total size of the directory
    result_decoded = result_decoded[1:]
    # remove the last line, which is the current working directory
    # result_decoded = result_decoded[:-1]
    return result_decoded


def get_current_shell():
    """
    Returns the unique identifier of the current shell. If no shell is currently active, creates a new shell and returns its identifier.

    Returns:
    str: The unique identifier of the current shell.
    """

    current_shell = get_memories("shell", "shell", filter_metadata={"current": "True"})

    if len(current_shell) == 0:
        shell_id = create_memory("shell", "shell", metadata={"current": "True"})
    else:
        current_shell = current_shell[0]
        shell_id = current_shell["id"]

    return shell_id


def set_cwd(cwd, shell_id=None):
    """
    Sets the current working directory of a specific shell.

    Parameters:
    cwd (str): The new current working directory.
    shell_id (str): The unique identifier of the shell. If not specified, uses the current shell.
    """

    if shell_id is None:
        shell_id = get_current_shell()
    shell = get_memory("shell", shell_id)
    metadata = shell["metadata"]
    metadata["cwd"] = cwd
    update_memory("shell", shell_id, metadata=metadata)


def set_current_shell(shell_id):
    """
    Sets the current shell to the shell with the specified identifier.

    Parameters:
    shell_id (str): The unique identifier of the shell to be made current.
    """

    current_shell_id = get_current_shell()
    if current_shell_id == shell_id:
        return

    current_shell = get_memory("shell", current_shell_id)
    current_shell["metadata"]["current"] = "False"
    update_memory("shell", current_shell["id"], metadata=current_shell["metadata"])

    shell = get_memory("shell", shell_id)
    shell["metadata"]["current"] = "True"
    update_memory("shell", shell_id, metadata=shell["metadata"])


def get_history(shell_id=None, n_limit=20):
    """
    Returns the command history of a specific shell.

    Parameters:
    shell_id (str): The unique identifier of the shell. If not specified, uses the current shell.
    n_limit (int): The maximum number of history entries to return.

    Returns:
    list: A list of dictionaries, each representing a command and its result.
    """

    if shell_id is None:
        shell_id = get_current_shell()
    history = get_memories(
        "shell_history", filter_metadata={"shell_id": shell_id}, n_results=n_limit
    )
    return history


def get_history_formatted(shell_id=None):
    """
    Returns the command history of a specific shell in a human-readable format.

    Parameters:
    shell_id (str): The unique identifier of the shell. If not specified, uses the current shell.

    Returns:
    str: The command history in human-readable format.
    """

    history = get_history(shell_id)
    formatted_history = ""
    for item in history:
        metadata = item["metadata"]
        formatted_history += "Command: " + metadata.get("command", "") + "\n"
        formatted_history += "Success: " + str(metadata.get("success", "")) + "\n"
        if "output" in metadata and metadata["output"].strip() != "":
            formatted_history += "Output: " + metadata["output"].strip() + "\n"
        if "error" in metadata and metadata["error"].strip() != "":
            formatted_history += "Error: " + metadata["error"].strip() + "\n"
        formatted_history += "---\n"  # separator between each command history
    return formatted_history


def add_to_shell_history(shell_id, command, success, output, error=None):
    """
    Adds a command and its result to the history of a specific shell.

    Parameters:
    shell_id (str): The unique identifier of the shell.
    command (str): The command that was executed.
    success (bool): Whether the command was successful.
    output (str): The output of the command.
    error (str): Any error messages produced by the command.
    """

    timestamp = time.time()

    formatted_memory = """\
    Command: {command}
    Timestamp: {timestamp}
    Success: {success}
    Output: {output}
    Error: {error}"""

    create_memory(
        "shell_history",
        formatted_memory,
        metadata={
            "shell_id": shell_id,
            "command": command,
            "success": success,
            "output": output or "",
            "error": error or "",
            "timestamp": timestamp,
        },
    )


def clear_history(shell_id):
    """
    Clears the command history of a specific shell.

    Parameters:
    shell_id (str): The unique identifier of the shell.
    """

    delete_memories("shell_history", metadata={"shell_id": shell_id})


def wipe_all():
    """
    Clears all shell and shell history data.
    """

    wipe_category("shell_history")
    wipe_category("shell")


def list_active_shells():
    """
    Returns a list of active shells.

    Returns:
    list: A list of shell identifiers.
    """

    shells = get_memories("shell")
    return [shell["id"] for shell in shells]


def close_shell(shell_id):
    """
    Closes a specific shell, clearing its history.

    Parameters:
    shell_id (str): The unique identifier of the shell.
    """

    delete_memories("shell_history", metadata={"shell_id": shell_id})
    delete_memory("shell", shell_id)


def new_shell():
    """
    Creates a new shell and returns its unique identifier.

    Returns:
    str: The unique identifier of the new shell.
    """

    shell_id = create_memory(
        "shell", "shell", metadata={"current": "False", "cwd": os.getcwd()}
    )
    return shell_id


def get_cwd(shell_id=None):
    """
    Returns the current working directory of a specific shell.

    Parameters:
    shell_id (str): The unique identifier of the shell. If not specified, uses the current shell.

    Returns:
    str: The current working directory of the shell.
    """

    if shell_id is None:
        shell_id = get_current_shell()
    shell = get_memory("shell", shell_id)
    return shell["metadata"]["cwd"]


def run_command(command, shell_id=None):
    """
    Runs a command in a specific shell and adds it to the shell's history.

    Parameters:
    command (str): The command to execute.
    shell_id (str): The unique identifier of the shell. If not specified, uses the current shell.

    Returns:
    bool: True if the command was successful, False otherwise.
    """

    if shell_id is None:
        shell_id = get_current_shell()
    shell = get_memory("shell", shell_id)
    cwd = shell["metadata"]["cwd"]
    # Execute command in the current working directory
    command_to_run = f"cd {cwd} && {command}"
    process = subprocess.run(command_to_run, shell=True, text=True, capture_output=True)

    # If the process completed successfully
    if process.returncode == 0:
        result = process.stdout

        result_split = result.strip().split("\n")
        updated_directory = result_split[-1]
        if os.path.isdir(updated_directory):
            cwd = updated_directory
            set_cwd(cwd, shell_id)
            result_split = result_split[:-1]
            result_split = "\n".join(result_split)
        else:
            result_split = "\n".join(result_split)

        add_to_shell_history(shell_id, command, success="True", output=result)
        return True

    else:  # If the process did not complete successfully
        output = process.stdout
        error = process.stderr
        add_to_shell_history(
            shell_id, command, success="False", output=output, error=error
        )
        return False
