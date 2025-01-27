import argparse
import os
import json
from datetime import datetime
import math

# ANSI escape codes for colors
BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

path_to_dir = 'D:/Python Projects/cmdPrograms/dist/'
filename = os.path.join(path_to_dir,"tasksplus.json")
bar_length = 40

def load_json_tasks(filename=filename):
    try:
        with open(filename,'r') as file:
            tasks = json.load(file)
        return tasks
    except Exception as e:
        print(e)

def save_json_tasks(tasks,filename=filename):
    try:
        with open(filename,'w') as file:
            json.dump(tasks,file,indent=4)
    except Exception as e:
        print(e)

def clear_completed_main_tasks():
    try:
        tasks = load_json_tasks()

        indices_to_remove = []

        i = 0
        for task in tasks["tasks"]:
            if task["complete"] == "yes":
                indices_to_remove.append(i)
            i += 1

        for index in sorted(indices_to_remove, reverse=True):
            del tasks['tasks'][index]

        save_json_tasks(tasks)
    except Exception as e:
        print(e)

def calculate_tasks_completion(main_id):
    try:
        tasks = load_json_tasks()
        counter = 0
        counter_complete = 0
        for brick_task in tasks["tasks"][main_id]["brick_tasks"]:
            if brick_task["complete"] == "yes":
                counter += 1
            counter_complete += 1

        c = 0
        if counter_complete != 0:
            c = math.floor((counter / counter_complete) * bar_length)
        return c
    
    except Exception as e:
        print(e)

def list_tasks():
    try:
        tasks = load_json_tasks()

        i = 0
        for task in tasks["tasks"]:
            task_completion = calculate_tasks_completion(i)
            if task["complete"] == "no":
                print(f"{RED}",end='')
            else:
                print(f"{GREEN}",end='')
            print(f"{i} | {task["title"]} | {task["expiration_date"]}")
            print(f"{RESET}|",end='')
            for j in range(task_completion):
                print(f"{GREEN}-",end='')
            for j in range(bar_length - task_completion):
                print(f"{RED}-",end='')
            print(f"{RESET}|")
            i += 1
    except Exception as e:
        print(e)

def list_brick_tasks(main_id):
    try:
        tasks = load_json_tasks()

        task_completion = calculate_tasks_completion(main_id)
        print(f"{BLUE}{tasks["tasks"][main_id]["title"]} | {tasks["tasks"][main_id]["expiration_date"]}")
        print(f"{RESET}|",end='')
        for j in range(task_completion):
            print(f"{GREEN}-",end='')
        for j in range(bar_length - task_completion):
            print(f"{RED}-",end='')
        print(f"{RESET}|")
        print()
        i = 0
        for task in tasks["tasks"][main_id]["brick_tasks"]:
            if task["complete"] == "no":
                print(f"{RED}",end='')
            else:
                print(f"{GREEN}",end='')
            print(f"{i} | {task["title"]} | {task["expiration_date"]}")
            i += 1
        print(f"{RESET}")
    except Exception as e:
        print(e)

# adding task with title, expiration date and brick_id if task is a part of group of task associated with main task (main_brick_task)
def add_task(title, expiration_date, brick_id):
    try:
        print(f"adding task {title} {expiration_date} {brick_id}")
        loaded_tasks = load_json_tasks()
        if brick_id == -1:
            loaded_tasks['tasks'].append({"title": title, "expiration_date": expiration_date, "complete" : "no", "brick_tasks": []})
        else:
            loaded_tasks['tasks'][brick_id]["brick_tasks"].append({"title": title, "expiration_date": expiration_date, "complete" : "no"})

        save_json_tasks(loaded_tasks)
    except Exception as e:
        print(e)

def check_main_completion(main_id):
    try:
        tasks = load_json_tasks()

        counter = 0
        counter_complete = 0
        for brick_task in tasks["tasks"][main_id]["brick_tasks"]:
            if brick_task["complete"] == "yes":
                counter += 1
            counter_complete += 1

        return counter == counter_complete
    except Exception as e:
        print(e)

def complete_task(main_id, brick_id):
    try:
        tasks = load_json_tasks()

        if brick_id == -1:
            tasks["tasks"][main_id]["complete"] = "yes"
            save_json_tasks(tasks)
            print(f"Main task {main_id} has been completed")
        else:
            tasks["tasks"][main_id]["brick_tasks"][brick_id]["complete"] = "yes"
            save_json_tasks(tasks)
            # check if all brick tasks completed
            if check_main_completion(main_id):
                tasks["tasks"][main_id]["complete"] = "yes"
                save_json_tasks(tasks)
            print(f"completing task {brick_id} of {main_id}")
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Console task manager")
    subparsers = parser.add_subparsers(dest='command')

    parser_ls = subparsers.add_parser('ls', help='Lists all tasks')
    parser_ls.add_argument('--task-id', '-id', type=int, help='Id of maintask to list brick tasks' )

    parser_add = subparsers.add_parser('add', help='Adds element + arg [--title, -t, --expire -e] date[d-m-y h:m]')
    parser_add.add_argument('--title', '-t', type=str,  help='Element to add')
    parser_add.add_argument('--expire', '-e', type=str,  help='Expiration date')
    parser_add.add_argument('--brick',  '-b', type=int, help="Brick task's id")

    parser_complete = subparsers.add_parser('complete', help='Delete arg with id + arg [--task-id ,-id] lub [--title ,-t]')
    parser_complete.add_argument('--task-id', '-id', type=int, help='ID of the main task to delete (or main task id if brick task is beeing deleted)')
    parser_complete.add_argument('--brick-task-id', '-bid', type=int, help='ID of the brick task to delete')
    parser_complete.add_argument('--title', '-t', type=str, help='Title of the task to delete')

    parser_clear_completed = subparsers.add_parser('clear', help='Delete all completed main tasks')

    args = parser.parse_args()

    if args.command == 'ls':
        if args.task_id is None:
            list_tasks()
        else:
            list_brick_tasks(args.task_id)
    elif args.command == 'add':
        if args.title is None:
            print("Title not provided")
            return
        if args.expire is None:
            print("Expiration date not provided")
            return
        if args.brick is None:
            add_task(args.title,args.expire,-1)
            return
        add_task(args.title,args.expire,args.brick)
    elif args.command == 'complete':
        if args.task_id is not None and args.brick_task_id is not None:
            complete_task(args.task_id,args.brick_task_id)
            return
        if args.task_id is not None:
            complete_task(args.task_id,-1)
            return
        print("main_task_id must be provided")
    elif args.command == 'clear':
        clear_completed_main_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()