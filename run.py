import argparse
import os

programs_path1 = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs" 
programs_path2 = "C:/Users/zaist/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"

def list_dir(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)

def list_apps():
    list_dir(programs_path1)
    list_dir(programs_path2)
    
def search_dir(partial_name, directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if partial_name.lower() in file.lower():
                full_path = os.path.join(root, file)
                try:
                    os.startfile(full_path)
                    print(f"{file} started")
                    return True
                except Exception as e:
                    print(f"Failed to start the application: {e}")
                    return False
    return False

def run_app(name):    
    if search_dir(name, programs_path1):
        return
    if search_dir(name, programs_path2):
        return

    print("No such file found.")

def main():
    parser = argparse.ArgumentParser(description="Console run app")
    subparsers = parser.add_subparsers(dest='command')

    parser_ls = subparsers.add_parser('ls', help='Lists all apps')

    parser_run_app = subparsers.add_parser('app', help='Runs app + arg [--name, -n]')
    parser_run_app.add_argument('--name', '-n', nargs=argparse.REMAINDER, type=str, required=True, help='App to run')

    args = parser.parse_args()

    if args.command == 'ls':
        list_apps()
    elif args.command == 'app':
        if hasattr(args, 'name'):
             app_name = ' '.join(args.name) if args.name else ''
             run_app(app_name)
        else:
            print("Task title not provided") 
    else:
        parser.print_help()

if __name__ == "__main__":
    main()