from repovisor import repovisor as rv
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Manage multiple repos')
    parser.add_argument('--search', '-s')
    parser.add_argument('--no_output', action='store_true')

    args = parser.parse_args()

    repos = []
    if args.search:
        repos += list(rv.reposearch(args.search))

    if not args.no_output:
        rv.print_all(*repos)
