import json
import markdown
from tabulate import tabulate

def format_as_table(json_response: str):
    """Formats JSON as a table"""
    try:
        data = json.loads(json_response)
        return tabulate([data.items()], headers=["Key", "Value"], tablefmt="grid")
    except Exception as e:
        return f"❌ Error formatting JSON: {str(e)}"

def format_as_card(markdown_response: str):
    """Formats Markdown as a simple card layout"""
    try:
        html_content = markdown.markdown(markdown_response)
        return f"<div class='card'>{html_content}</div>"
    except Exception as e:
        return f"❌ Error formatting Markdown: {str(e)}"
