import datetime


def args_parse(args):
    parsed = {}
    a = "asd"
    a
    for i, _ in enumerate(args):
        if args[i].startswith("--"):
            name = args[i].split("--")[1]
            parsed[name] = args[i+1]
    return parsed
