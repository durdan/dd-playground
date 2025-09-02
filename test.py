#!/usr/bin/env python3

def read_and_print_hello():
    """Read content from hello.txt and print it."""
    try:
        with open('hello.txt', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            print(content)
    except FileNotFoundError:
        print("Error: hello.txt file not found")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    read_and_print_hello()