from colorama import Fore, Style


class Logger:
    def __init__(self, log_func=None):
        self.log_func = log_func
        self.colors = Fore
        self.reset_all = Style.RESET_ALL

    def log(self, *kwargs):
        self.log_func(*kwargs, f"{lg.reset_all}")


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__(log_func=print)


if __name__ == "__main__":
    lg = ConsoleLogger()
    lg.log(f"{lg.colors.CYAN}hello", "hi")