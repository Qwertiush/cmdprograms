import argparse
import webbrowser
import urllib.parse

path = "https://www.wolframalpha.com/input?i="

def solve_equation(equation):
    equation = ''.join(equation)

    encoded_equation = urllib.parse.quote(equation)
    
    fullPath = path + encoded_equation
    webbrowser.open(fullPath)


def main():
    parser = argparse.ArgumentParser(description="Console calculation with Wolfram Alpha app.")
    subparsers = parser.add_subparsers(dest='command')

    parser_run_app = subparsers.add_parser('equation', help='Solves equation + arg [--string, -s]')
    parser_run_app.add_argument('--string', '-s', nargs=argparse.REMAINDER, type=str, required=True, help='Equation to solve.')

    args = parser.parse_args()

    if args.command == 'equation':
        if hasattr(args, 'string'):
             solve_equation(args.string)
        else:
            print("Task title not provided") 
    else:
        parser.print_help()

if __name__ == "__main__":
    main()