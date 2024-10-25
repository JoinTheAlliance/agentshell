# agentshell

A shell for your agent. Track state and history, multiple shells, and more.

<img src="resources/image.jpg">

[![Lint and Test](https://github.com/AutonomousResearchGroup/agentshell/actions/workflows/test.yml/badge.svg)](https://github.com/AutonomousResearchGroup/agentshell/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/agentshell.svg)](https://badge.fury.io/py/agentshell)

# Installation

```bash
pip install agentshell
```

# Getting Started

`agentshell` is a shell wrapper around `subprocess` for maintaining command history and current working directory across multiple shell instances.

### Basic Usage

**Starting with the default shell**:

If you don't specify a shell ID, `agentshell` will use a default shell.

```python
from agentshell import run_command

response = run_command('ls')
print(response['output'])
```

**Getting Current Working Directory**:

Fetch the current directory of the active shell:

```python
from agentshell import get_cwd

current_directory = get_cwd()
print(current_directory)
```

**Setting Current Working Directory**:

You can also change the directory of the active shell:

```python
from agentshell import set_cwd

set_cwd('/path/to/directory')
```

### Advanced Usage

**Managing Multiple Shells**:

With `agentshell`, it's straightforward to handle multiple shell instances.

- **Creating a new shell**:

```python
from agentshell import new_shell

shell_id = new_shell()
```

- **Listing active shells**:

```python
from agentshell import list_active_shells

shells = list_active_shells()
print(shells)
```

- **Switching between shells**:

```python
from agentshell import set_current_shell

set_current_shell(shell_id)
```

- **Closing a shell**:

```python
from agentshell import close_shell

close_shell(shell_id)
```

**Viewing Command History**:

You can view the command history of any shell. If no shell ID is provided, it fetches the history of the current active shell.

```python
from agentshell import get_history_formatted

formatted_history = get_history_formatted()
print(formatted_history)
```

**Clearing History**:

```python
from agentshell import clear_history

clear_history(shell_id)
```

**Running Commands in a Specific Shell**:

Run commands in a shell by specifying its ID.

```python
from agentshell import run_command

response = run_command('echo "Hello, World!"', shell_id=shell_id)
print(response['output'])
```

# Documentation

## `get_files_in_cwd(shell_id=None)`

Returns a list of files in the current directory of a specific shell. If `shell_id` is not specified, uses the current shell.

**Parameters:**

- `shell_id`: The unique identifier of the shell.

**Returns:**

- A list of filenames in the current directory.

## `get_current_shell()`

Returns the unique identifier of the current shell. If no shell is currently active, creates a new shell and returns its identifier.

**Returns:**

- The unique identifier of the current shell.

## `set_cwd(cwd, shell_id=None)`

Sets the current working directory of a specific shell. If `shell_id` is not specified, uses the current shell.

**Parameters:**

- `cwd`: The new current working directory.
- `shell_id`: The unique identifier of the shell.

## `set_current_shell(shell_id)`

Sets the current shell to the shell with the specified identifier.

**Parameters:**

- `shell_id`: The unique identifier of the shell to be made current.

## `get_history(shell_id=None, n_limit=20)`

Returns the command history of a specific shell. If `shell_id` is not specified, uses the current shell.

**Parameters:**

- `shell_id`: The unique identifier of the shell.
- `n_limit`: The maximum number of history entries to return.

**Returns:**

- A list of dictionaries, each representing a command and its result.

## `get_history_formatted(shell_id=None)`

Returns the command history of a specific shell in a human-readable format. If `shell_id` is not specified, uses the current shell.

**Parameters:**

- `shell_id`: The unique identifier of the shell.

**Returns:**

- The command history in human-readable format.

## `add_to_shell_history(shell_id, command, success, output, error=None)`

Adds a command and its result to the history of a specific shell.

**Parameters:**

- `shell_id`: The unique identifier of the shell.
- `command`: The command that was executed.
- `success`: Whether the command was successful.
- `output`: The output of the command.
- `error`: Any error messages produced by the command.

## `clear_history(shell_id)`

Clears the command history of a specific shell.

**Parameters:**

- `shell_id`: The unique identifier of the shell.

## `wipe_all()`

Clears all shell and shell history data.

## `list_active_shells()`

Returns a list of active shells.

**Returns:**

- A list of shell identifiers.

## `close_shell(shell_id)`

Closes a specific shell, clearing its history.

**Parameters:**

- `shell_id`: The unique identifier of the shell.

## `new_shell()`

Creates a new shell and returns its unique identifier.

**Returns:**

- The unique identifier of the new shell.

## `get_cwd(shell_id=None)`

Returns the current working directory of a specific shell. If `shell_id` is not specified, uses the current shell.

**Parameters:**

- `shell_id`: The unique identifier of the shell.

**Returns:**

- The current working directory of the shell.

## `run_command(command, shell_id=None)`

Runs a command in a specific shell and adds it to the shell's history. If `shell_id` is not specified, uses the current shell.

**Parameters:**

- `command`: The command to execute.
- `shell_id`: The unique identifier of the shell.

**Returns:**

- `True` if the command was successful, `False` otherwise.

# Contributions Welcome

If you like this library and want to contribute in any way, please feel free to submit a PR and I will review it. Please note that the goal here is simplicity and accesibility, using common language and few dependencies.
