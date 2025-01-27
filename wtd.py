import argparse
import os
import json
from datetime import datetime
import math

path_to_dir = 'D:/Python Projects/cmdPrograms/dist/'
tasksPath = os.path.join(path_to_dir, 'tasks.txt')
configPath = os.path.join(path_to_dir, 'config.json')
separator = "7^%7"

# ANSI escape codes for colors
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

def get_config(filename=configPath):
    try:
        with open(filename, 'r') as file:
            # Parse the JSON data into a Python dictionary
            config_data = json.load(file)
            return config_data
    except FileNotFoundError:
        print("File can't be found")
    except json.JSONDecodeError:
        print("Error decoding JSON")
    except Exception as e:
        print(f"An error occurred: {e}")

def set_config(new_config, filename=configPath):
    try:
        with open(filename, 'w') as file:
            # Convert the Python dictionary to JSON and write it to a file
            json.dump(new_config, file, indent=4)  # indent for pretty printing
    except FileNotFoundError:
        print("File can't be found")
    except IOError:
        print("IO error occurred")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_date():
    today = datetime.now()
    return today

def add_element(element, exp_date, filename=tasksPath):
    try:
        element = str(element)
        with open(filename, 'a') as file:
            file.write(element + separator + exp_date + separator + get_date().strftime('%d-%m-%Y %H:%M') + "\n")
    except TypeError:
        print("Element can't be converted to string.")
    except IOError:
        print("Error while saving file")

def get_tasks_from_file(filename=tasksPath):
    try:
        lines = []

        with open(filename, 'r') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {filename}")
    except IOError:
        print("Wystąpił błąd podczas odczytu pliku.")

def list_tasks(filename=tasksPath):
    lines = get_tasks_from_file()
    for i in range(len(lines)):
        params = lines[i].strip().split(separator)
        title = params[0]
        exp_date = datetime.strptime(params[1], "%d-%m-%Y %H:%M")
        start_date = datetime.strptime(params[2], "%d-%m-%Y %H:%M")
        
        # Calculate time differences
        total_time = (exp_date - start_date).total_seconds()
        time_passed = (get_date() - start_date).total_seconds()
        
        # Ensure we don't divide by zero if start_date and exp_date are the same
        if total_time > 0:
            time_difference = time_passed / total_time
        else:
            time_difference = 0
        
        max_value = 40
        time_difference *= max_value

        
        # Print output
        print(f"{i} | {title} | {exp_date.strftime('%d-%m-%Y %H:%M')}",end='')
        dash_chars_nbr = math.floor(time_difference)
        if dash_chars_nbr > max_value:
            dash_chars_nbr = max_value
            print(f' {RED}[expired]{RESET}')
        else:
            print('')
        print('|',end='')
        for i in range(dash_chars_nbr):
            print(f'{GREEN}-',end='')
        for i in range(max_value - dash_chars_nbr):
            print(f'{RED}-',end='')
        print(f'{RESET}|')
#todo change active task id when other task deleted
def complete_task(item_id, filename=tasksPath):
    
    lines = []
    with open(filename, 'r') as file:
        lines = file.readlines()

    if item_id >= len(lines):
        print("You're out of range ;). Try again.")
        return

    task = lines[item_id].strip()
    del lines[item_id]

    with open(filename, 'w') as file:
        file.writelines(lines)

    print("Congratulations, you've compleated " + task)

def get_active_task(filename=tasksPath):
    lines = get_tasks_from_file()
    config = get_config()

    taskId = config['activeTask']
    if taskId < 0:
        print("active task is not set :)")
        return
    if taskId >= len(lines):
        print("No such an id")
        return
    
    print(f"Your's active task is [{lines[taskId].strip()}]");

def set_active_task(id):
    config = get_config()
    tasks = get_tasks_from_file()

    if id >= len(tasks):
        print("There is no such an ID ;)")
        return

    config['activeTask'] = id
    set_config(config)

    get_active_task()

def complete_active_task(s):
    if not (s=="yes" or s=="y"):
        return
    
    config = get_config()

    complete_task(config['activeTask'])

    set_active_task(-1)

def main():
    parser = argparse.ArgumentParser(description="Console task manager")
    subparsers = parser.add_subparsers(dest='command')

    parser_ls = subparsers.add_parser('ls', help='Lists all tasks')

    parser_add = subparsers.add_parser('add', help='Adds element + arg [--title, -t, --expire -e] date[d-m-y h:m]')
    parser_add.add_argument('--title', '-t', type=str,  help='Element to add')
    parser_add.add_argument('--expire', '-e', type=str,  help='Expiration date')

    parser_complete = subparsers.add_parser('complete', help='Delete arg with id + arg [--task-id ,-id] lub [--title ,-t]')
    parser_complete.add_argument('--task-id', '-id', type=int, help='ID of the task to delete')
    parser_complete.add_argument('--title', '-t', type=str, help='Title of the task to delete')

    parser_set_active = subparsers.add_parser('active', help='Sets active task + arg [--task-id, -id, --complete, -c]')
    parser_set_active.add_argument('--task-id', '-id', type=int, help='ID of the active task')
    parser_set_active.add_argument('--complete', '-c', type=str, help='Complete active task')

    args = parser.parse_args()

    if args.command == 'ls':
        list_tasks()
    elif args.command == 'add':
        if args.title is not None and args.expire is not None:
            add_element(args.title, args.expire)
        else:
            print("Task title or expiration date not provided") 
    elif args.command == 'complete':
        if args.task_id is not None:
            complete_task(args.task_id)
        elif args.title is not None:
            print(f"Deleting task with title: {args.title} (out of order)")
        else:
            print("Error: You must provide either --task-id or --title.")
            parser_complete.print_usage()
    elif args.command == 'active':
        if args.task_id is not None:
            set_active_task(args.task_id)
        elif args.complete is not None:
            complete_active_task(args.complete)
        else:
            get_active_task()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
