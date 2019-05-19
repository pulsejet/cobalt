# Cobalt ![Logo](./logo.svg)

Cobalt is a minimalistic no-nonsense tool to send out customized mail with conversion tracking.

## Features
* Email templates with variables
* Background processing of emails
* Mail tracking with 1x1 `img`
* WYSIWYG template editor
* Error tracking, resend individual emails
* A minimalistic, productivity oriented UI

## Usage
Run as any other django with celery app. On Windows, use `celery -A cobalt worker --pool=solo -l info` for testing.
