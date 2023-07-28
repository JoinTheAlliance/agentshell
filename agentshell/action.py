from easycompletion import compose_function, compose_prompt

from agentshell.main import get_files_in_current_directory, run_command


use_shell_prompt = """TIME: {{current_time}}
DATE: {{current_date}}
PLATFORM: {{platform}}
PROJECT DIRECTORY: {{cwd}}
PWD: {{cwd}}
{{files_in_current_directory}}
{{relevant_knowledge}}
{{events}}
{{summary}}
{{reasoning}}
TASK: Based on the action reasoning, what command should I run in my terminal? Please include all arguments, etc. on one line.
- Write a one-liner that I can run in my terminal (command)
- Then, write a summary of what output you expect to see (expected_output)
- If I ran a command, I probably should not run it again, so please don't suggest the same command twice in a row. Since you already know the cwd and files in the current directory, you shouldn't just run ls or pwd.
- DO NOT suggest running any commands that will provide us with the same information we already have. For example, if we already know the current working directory, don't suggest running pwd.
"""


def compose_use_shell_prompt(context):
    context["files_in_current_directory"] = (
        "\n" + "Files in the current directory (ls -alh):\n"
        "============================================\n"
        "" + ("\n".join(get_files_in_current_directory())) + "\n"
        "============================================\n"
    )

    return compose_prompt(use_shell_prompt, context)


def use_shell(arguments):
    command = arguments.get("command")
    run_command(command)


def get_actions():
    return [
        {
            "function": compose_function(
                name="use_shell",
                description="Run a command in my terminal. I can use this to access my operating system and interact with the world, or to call some code. This is a full terminal, so any code that works in bash will work.",
                properties={
                    "command": {
                        "type": "string",
                        "description": "The full command to run in my shell, including all arguments, etc.",
                    },
                    "expected_output": {
                        "type": "string",
                        "description": "Describe the expected output of the command. Write it from the user's perspective, in the first person, e.g. 'I should see the current working directory.'",
                    },
                },
                required_properties=["command", "expected_output"],
            ),
            "prompt": use_shell_prompt,
            "builder": compose_use_shell_prompt,
            "handler": use_shell,
            "suggestion_after_actions": ["use_shell"],  # suggest self
            "never_after_actions": [],
        }
    ]
