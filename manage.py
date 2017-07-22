#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault(u"DJANGO_SETTINGS_MODULE", u"book.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
