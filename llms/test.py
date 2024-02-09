import pprint
from llama_index.llms import LlamaCPP
from llama_index.llms.base import ChatMessage

def pretty_print_string(string, indent=4, replace_tabs=True):
    """
    Pretty prints a string by replacing `\n` with newlines, adding indentation,
    and handling tabs optionally.

    Args:
    string: The string to be pretty printed.
    indent (int, optional): Number of spaces for indentation (default: 4).
    replace_tabs (bool, optional): Whether to replace tabs with spaces (default: True).

    Returns:
    The pretty printed string.
    """

    # Replace `\n` with newlines
    string = string.replace("\\n", "\n")

    # Handle tabs with spaces if desired
    if replace_tabs:
        string = string.replace("\t", " " * indent)

    # Add indentation based on nesting level
    indented_string = ""
    indent_level = 0
    for line in string.splitlines():
        if line.startswith("  "):
            indent_level += 1
        elif line.startswith("-"):
            indent_level -= 1
    indented_string += " " * indent_level * indent + line + "\n"

    return indented_string

model_path="/Users/titan/Downloads/llama-2-13b-chat.Q5_K_M.gguf"
llm_gpt=LlamaCPP(model_path=model_path)

message=ChatMessage(role="user",content="Write a 2 page platform engineer resume that includes tools like argocd, kubernetes and helm.  It should include at least 4 public company names and a description of the type of team i worked with and what I was doing.")
message=ChatMessage(role="user",content="write a python script that scrapes the Sumologic API and downloads monitor information")
response = llm_gpt.chat([message])
print(response.message.content)
pretty_print_string(response.message.content)

# Print the response
