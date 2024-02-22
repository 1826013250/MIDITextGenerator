from menu import *
from time import sleep
from wrappers import safe_exception


class MyApp:
    @safe_exception
    def __init__(self):
        """初始化对象"""
        self.version = "0.0"
        self.name = "MIDI Text Generator"
        self.__initscr()
        use_default_colors()
        self.__init_color()
        self.max_rows, self.max_columns = self.scr.getmaxyx()
        self.__init_windows()

    def exit(self):
        self.scr.keypad(False)
        nocbreak()
        echo()
        endwin()

    def main(self):
        self.menu.select()

    @safe_exception
    def __initscr(self) -> None:
        self.scr = initscr()
        noecho()
        cbreak()
        self.scr.keypad(True)
        if has_colors():
            start_color()
        else:
            print("This terminal environment seems does not support color.\n"
                  "Limited functions proceed.\n"
                  "This message will disappear in 3 seconds.")
            sleep(3)

    def __init_color(self):
        init_pair(1, COLOR_YELLOW, -1)
        init_pair(2, COLOR_MAGENTA, -1)
        init_pair(3, COLOR_GREEN, -1)

        self.C_YELLOW = color_pair(1)
        self.C_MAGENTA = color_pair(2)
        self.C_GREEN = color_pair(3)

    @safe_exception
    def __init_windows(self):
        self.infowin = newwin(2, self.max_columns)
        self.infowin.addstr("[", self.C_YELLOW)
        self.infowin.addstr(self.name, self.C_MAGENTA)
        self.infowin.addstr("]", self.C_YELLOW)
        self.infowin.addstr(f" v{self.version}\n")
        self.infowin.addstr("当前文件: ", self.C_GREEN)
        self.filename = None
        self.infowin.addstr(self.filename if self.filename else "无")
        self.info_panel = new_panel(self.infowin)
        update_panels()
        doupdate()
        self.menu = Menu(newwin(self.max_rows - 2, self.max_columns, 2, 0), {
            "setmid": "选择文件",
            "play": "播放所选mid文件",
            "out": "输出乐谱",
            "settings": "设置",
            "quit": "退出"
        }, style="PREFIX", select_color=(-1, COLOR_GREEN))


if __name__ == '__main__':
    app = MyApp()
    app.main()
