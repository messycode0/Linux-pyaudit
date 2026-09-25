import shutil

def print_barrier():
    # gets the length of the terminal print == 
    terminal_width = shutil.get_terminal_size(fallback=(80, 24))[0]

    print("-" * terminal_width)

def print_banner(text):
    terminal_width = shutil.get_terminal_size(fallback=(80, 24))[0]

    print("-" * terminal_width)
    print(f"{text:^{terminal_width}}")
    print("-" * terminal_width)

def print_small_title(text):
    terminal_width = shutil.get_terminal_size(fallback=(80, 24))[0]
    # print(f"====== {text} ======":^terminal_width)
 
    print(f"{'=' * ((terminal_width - len(text)) // 2)}{text}{'=' * ((terminal_width - len(text)) // 2)}")

if __name__ == "__main__":
    print("run the RUNNER.PY script -_-")
