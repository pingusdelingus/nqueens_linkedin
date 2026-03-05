
from colorama import init, Fore, Back, Style




Fore.ORANGE = '\x1b[38;5;208m'

int_to_color = [
        #0         #1        #3            #4        #5             #6                # 7         #8          #9           #10
      Fore.GREEN, Fore.RED,Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.LIGHTCYAN_EX, Fore.WHITE,Fore.BLACK, Fore.ORANGE,  Fore.RESET
]
reset = int_to_color[len(int_to_color) - 1]

init(autoreset=True)
class Square():
    def __init__(self, color, hasQ):
        self.color_int = color
        self.color = f"{int_to_color[color]}X{reset}"
        self.hasQ = hasQ


    def __str__(self):
        return str(self.color)

    def hasQueen(self):
        return self.hasQ

    def setQueen(self):
        self.color = f"{int_to_color[self.color_int]}Q{reset}"
        self.hasQ = True

    def setEmpty(self):
        self.color = f"{int_to_color[self.color_int]}X{reset}"
        self.hasQ = False


