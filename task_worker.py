#!/usr/bin/env python
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cobalt.settings")
    import django_tasker.worker
    django_tasker.worker.main()
