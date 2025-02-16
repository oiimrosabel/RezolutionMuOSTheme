import sys


def task(text: str):
    print(f"▶️ > {text}")


def info(text: str):
    print(f"\tℹ️ > {text}")


def warning(text: str):
    print(f"\t⚠️ > {text}", file=sys.stderr)


def error(text: str):
    print(f"\t🛑 > {text}", file=sys.stderr)


def success(text: str):
    print(f"\t✅ > {text}")


def ask(text: str, choices: list, default=0) -> int:
    question = f"\n❓️ > {text} (default = {default}) \n"
    for i, c in enumerate(choices):
        question += f"\t{i} : {c}\n"
    question += "\n❗️ < "
    res = input(question)
    if res == "":
        print(f"❗️ > Chose {choices[default]} ({default}, default)\n")
        return default
    try:
        res = int(res)
    except ValueError:
        error("Invalid input. Try again.")
        return ask(text, choices, default)
    if res < 0 or res > len(choices):
        error("Invalid input. Try again.")
        return ask(text, choices, default)
    print(f"❗️ > Chose {choices[res]} ({res})\n")
    return res
