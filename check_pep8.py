#!/usr/bin/env python
import subprocess

subprocess.call(['flake8', '--exclude', 'env', '.'])
