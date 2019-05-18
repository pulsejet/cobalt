"""Cobalt renderer."""
import datetime
import html
import json
from django.conf import settings

def cobalt_render(template: str, values: str) -> str:
    """Render a template to the email."""

    # Convert json to dict
    values = json.loads(values)

    # Variable substitution
    for col in values:
        template = template.replace('{{' + col + '}}', values[col])

    return template

def mailtrack(rendered: str, mid: str) -> str:
    """Add mailtrack image to a rendered template."""
    return rendered + str(' <img style="opacity: 0.05" src="%smt/%s" /> ' % (settings.FULL_ROOT_PATH, mid))

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
