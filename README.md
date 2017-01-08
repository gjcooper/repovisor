# The Repository Supervisor

version number: 0.0.1
author: Gavin Cooper

## Overview

A tool for supervising multiple repositories, checking their status and providing regular reminders of unfinished work.

# Who is it for

This tool is primarily designed for those developers or repository users who may have multiple (read 10+) repositories all possibly being touched during a day. It's main benefit will be providing a regular report of repositories that are in an uncomitted/unpushed or unpulled state, allowing you to write your commit messages and push your local changes whilst the work is still fresh in your mind.

# Installation / Usage

To install use pip:

    $ pip install repovisor


Or clone the repository:

    $ git clone https://github.com/gjc216/repovisor.git
    $ python setup.py install

As a manually run script, or added as a cron job it will provide a status for all repositories in it's internal database, showing the results either within a terminal, or as a web generated report
    
# Example

TBD

# Technology Stack

Written in python, it is based off the GitPython package , providing user facing UI features

Currently the VCS it supports is:
* Git
* -Mercurial-
* -Subversion-

# Contributing

TBD
