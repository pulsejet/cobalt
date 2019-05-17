"""Cobalt renderer."""
import json

def cobalt_render(template: str, values: str) -> str:
    """Render a template to the email."""

    # Convert json to dict
    values = json.loads(values)

    # Variable substitution
    for col in values:
        template = template.replace('{{' + col + '}}', values[col])

    return template
