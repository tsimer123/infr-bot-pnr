import sys
from sql.scheme import create_db
from bot.start_bot import run_bot


def first_start():
    create_db()


def start_bot():
    create_db()
    run_bot()


def main():
    input_flags = sys.argv
    # input_flags = [0, "-start_b"]

    try:
        if input_flags[1] == "-help":
            print("-help - help\n-start_b - start bot\n-crt_db  - create db")

        if input_flags[1] == "-start_b":
            start_bot()

        if input_flags[1] == "-crt_db":
            first_start()
    except Exception as ex:
        print(str(ex.args))
        print("-help - help\n-start_b - start bot\n-crt_db  - create db")


if __name__ == "__main__":
    main()