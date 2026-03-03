
from colorama import init, Fore, Back, Style



int_to_color = [
      Fore.GREEN, Fore.RED,Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.LIGHTCYAN_EX, Fore.WHITE,Fore.BLACK, Fore.RESET
]
reset = int_to_color[len(int_to_color) - 1]

init(autoreset=True)
class Square():
    def __init__(self, color, hasQ):
        self.color = f"{int_to_color[color]}X{reset}"
        self.hasQ = hasQ


    def __str__(self):
        return str(self.color)

    def hasQueen(self):
        return self.hasQ

    def setQueen(self):
        self.color = f"{int_to_color[color]}Q{reset}"

    def setEmpty(self):
        self.color = f"{int_to_color[color]}X{reset}"


