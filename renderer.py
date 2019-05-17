"""Cobalt renderer."""
import datetime
import html
import json

def cobalt_render(template: str, values: str) -> str:
    """Render a template to the email."""

    # Convert json to dict
    values = json.loads(values)

    # Variable substitution
    for col in values:
        template = template.replace('{{' + col + '}}', values[col])

    return template

def get_log_mail(mail, rendered: str) -> str:
    return '''\
<pre style="white-space: pre-wrap;">
Subject: %s
From: %s
Timestamp: %s
</pre>

%s''' % (html.escape(mail.campaign.subject),
         html.escape(mail.campaign.from_email),
         str(datetime.datetime.now()), rendered)
