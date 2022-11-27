"""Generate random todos
"""
import sys
import random
import argparse
import requests


def word_generator(k):
    """Generates random todo.title
    """
    chrs = "abcdefghijklmnoprstuvwxyz"
    return f"autoTodo{str(k)}_{''.join(random.choices(chrs, k=7))}"



def parse_args(args):
    """Parsing command arguments
    """
    parser = argparse.ArgumentParser(description="Todos generator",
                                     add_help=True, epilog="Glebas corporation",
                                     formatter_class=argparse.HelpFormatter)
    composing = parser.add_argument_group("Number of todos",
                                          "Генерация тудушек в журнал (без аргумента, создаст 20)")
    composing.add_argument("--number", dest="number", nargs="*",
                           help="добавляет <num> тудушек в журнал", metavar="num")
    return parser.parse_intermixed_args(args)

def main():
    """Generator of todos
    """
    cli_args = sys.argv[1:]
    args = parse_args(cli_args)
    if args.number is None:
        print("Generating 20 todos")
        for i in range(20):
            requests.post("http://0.0.0.0/add", {"title": word_generator(i+1)})
    if args.number is not None:
        print(f"Generating {args.number[0]} todos")
        for i in range(int(args.number[0])):
            requests.post("http://0.0.0.0/add", {"title": word_generator(i+1)})


if __name__ == "__main__":
    main()
