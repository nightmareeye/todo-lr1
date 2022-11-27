import sys
import random
import requests
import argparse

def word_generator():
    chrs="abcdefghijklmnoprstuvwxyz"
    return "autoTodo_" + ''.join(random.choices(chrs,k=7))

def parse_args(args):
    parser = argparse.ArgumentParser(description="Todos generator", add_help=True, epilog="Glebas corporation",
                                     formatter_class=argparse.HelpFormatter)
    composing = parser.add_argument_group("Number of todos",
                                          "Генерация тудушек в журнале (без указания аргумента, сгенерирует 20)")
    composing.add_argument("--number", dest="number",  nargs="*", help="добавляет <num> тудушек в журнал", metavar="num")
    return parser.parse_intermixed_args(args)

def main():
    cli_args = sys.argv[1:]
    args = parse_args(cli_args)
    print(f"I am run {args.number}")
    if args.number is None:
        for i in range(20):
            requests.post("http://localhost/add", {"title" : word_generator() })
    if args.number is not None:
         for i in range(int(args.number[0])):
            requests.post("http://localhost/add", {"title": word_generator()})

if __name__ == "__main__":
    main()