import random
import time as t
import sys
import os

spam_help = [
    "-------------------------------------------------- <> HELP <> --------------------------------------------------",
    "[any number]:      |amount|    defines the amount of Spam Files !! Should always be at the end of the commands !!",
    "[-i]:              |info|      gives out more information while running",
    "[-e]:              |empty|     create empty files",
    "[-m]:              |message|   manual define of your File-Name (takes single argument after indicator)",
    "[-P](uppercase):   |path|      manual define of your target path/paths (takes multiple arguments before executing)",    # nopep8
    "[-p]:              |path|      manual define of your target path/paths (takes single argument after indicator)",
    "[c]:               |clear|     clear your Terminal-Window",
    "[h]/[help]:        |help|      shows current help output",
    "[exit]:            |exit|      exit the programm",
    "-------------------------------------------------- <> HELP <> --------------------------------------------------"
]

lines = open("words_1000.txt").read().splitlines()

if sys.platform == "win32":
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
elif sys.platform == "linux":
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
else:
    print("Invalid operating System")
    exit()


def cf(progress_name, output="", leading_output=""):
    c_time = t.asctime()
    console_format = f'{leading_output}[{c_time[c_time.find(":") - 2: c_time.find(":") + 6]}]{sys.platform} || {progress_name} -> {output}'     # nopep8
    return console_format


def create_files(amount, details=False, msg=None, given_path=None):
    if msg:
        file_name = msg
    else:
        file_name = rnd_word

    if given_path:
        data_path = f"{given_path}/{file_name}"
    else:
        data_path = f"{desktop}/{file_name}"

    for x in range(1, amount + 1):
        open(f"{data_path}({x}).txt", "x")

        if details:
            print(cf("Spam", f"Created Files: ({x}/{amount}) || Blocked Space: {(x * 0.0000001):.03} GB || '{data_path}({x}).txt'"))    # nopep8
        else:
            print(cf("Spam", f"Created Files: ({x}/{amount})"))


def fill_files(amount, details=False, msg=None, given_path=None):
    if msg:
        file_name = msg
    else:
        file_name = rnd_word

    if given_path:
        data_path = f"{given_path}/{file_name}"
    else:
        data_path = f"{desktop}/{file_name}"

    for x in range(1, amount + 1):
        with open(f"{data_path}({x}).txt", "w") as file:
            for line in open("words.txt", "r+"):
                file.write(line)
            if details:
                print(cf("Spam", f"Filled Files: ({x}/{amount}) || Blocked Space: {(x * 0.100033):.03} GB || '{data_path}({x}).txt' used 'words.txt'"))   # nopep8

            else:
                print(cf("Spam", f"Filled Files: ({x}/{amount})"))


def spam(amount, details=False, empty=False, msg=None, path_list=None):
    if len(path_list) == 0:
        path_list.append(desktop)

    for current_path in path_list:
        create_files(amount, details, msg, current_path)
        if not empty:
            fill_files(amount, details, msg, current_path)
            print(cf("Spam"))
            print(cf("Spam", f"Spam finished within {(t.time() - start):.04} sec.\n\n"))

        else:
            print(cf("Spam"))
            print(cf("Spam", f"Blocked Space: {(amount * 0.100033):.03} GB"))
            print(cf("Spam", f"Spam finished within {(t.time() - start):.04} sec.\n\n"))


while True:
    user_input = input(cf("Spam"))
    user_input = user_input.split()
    infos_queued = False
    empty_queued = False
    message = ""
    path = []
    next_command_not_valid = False
    for command in user_input:
        if next_command_not_valid:
            next_command_not_valid = False
            continue

        if command == "exit":
            exit()

        elif command == "c":
            for clear_index in range(0, 200):
                print()

        elif command == "h" or command == "help":
            print(cf("Spam", ""))
            print(cf("Spam", ""))
            for help_line in spam_help: print(cf("HELP", help_line))
            print(cf("Spam", ""))
            print(cf("Spam", ""))

        else:
            if command == "-i":
                infos_queued = True

            elif command == "-e":
                empty_queued = True

            elif command == "-m":
                message = user_input[user_input.index(command) + 1]  # takes next argument
                next_command_not_valid = True

            elif command == "-P":
                while True:
                    user_path = input(cf("Spam", "Your Path:\t"))
                    if not user_path:
                        break
                    path.append(user_path)

            elif command == "-p":
                path.append(user_input[user_input.index(command) + 1])   # takes next argument
                next_command_not_valid = True

            elif command.isnumeric():
                print(cf("Spam", f"Estimated Time: {int(command) * 6} sec."))
                rnd_word = random.choice(lines)
                t.sleep(3)
                print(cf("Spam", "Starting..."))
                start = t.time()
                spam(int(command), infos_queued, empty_queued, message, path)

            else:
                print(cf("Spam", f"Invalid Command: '{command}'"))
