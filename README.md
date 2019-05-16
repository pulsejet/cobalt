# Cobalt
Cobalt is a simple UI to send out bulk emails to people with simple mailmerge like tech, from a local SMTP server.

# Usage
Run as any other django with celery app. On Windows, use `celery -A cobalt worker --pool=solo -l info` for testing.
