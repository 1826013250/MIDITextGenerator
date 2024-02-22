from curses import *
from curses.panel import *
import _curses
from typing import Union, Tuple


class Menu:
    def __init__(self,
                 win: _curses.window,
                 selections: dict,
                 style: str = "CONTRAST",
                 select_color: Tuple[int, int] = (-1, -1),
                 unselect_color: Tuple[int, int] = (-1, -1),
                 prefix: str = ">",
                 align: bool = False) -> None:
        """
        传入一个_CursesWindow对象，对其添加指定菜单。

          win
            传入的_CursesWindow对象。
          selections
            接受一个字典，字典的key将为选中时的返回值，value为显示在菜单中的文字。默认为。
          style
            接受一个字符串，调整菜单突出显示选中项的方式，默认为CONTRAST。可选参数如下：

            CONTRAST
              使用curses.A_STANDOUT进行突出显示。
            PREFIX
              在选中项目前添加prefix所指定的字符。
            COLORED
              对突出显示的对象进行颜色修饰。（不进行任何样式修改，使用select_color指定颜色）
          prefix
            接受一个字符串。当style为PREFIX的时候为突出显示的菜单前缀。默认为">"。
          select_color
            接受一个元组，设定被选中的选项的颜色。元组格式为(前景色（字体色）, 背景色)，默认为(-1, -1)
          unselect_color
            接受一个元组，设定未选中的选项的颜色。元组格式同上，默认为(-1, -1)
          align
            接受一个布尔值，将所有选项内容对齐。默认为False。
          :return: 无/该class的实例
        """
        use_default_colors()
        self.win = win
        self.panel = new_panel(win)
        self.win.keypad(True)
        self.max_rows, self.max_columns = win.getmaxyx()
        self.menu = selections
        self.style = style
        self.prefix = prefix
        self.align = align
        self.select_color = select_color
        self.unselect_color = unselect_color
        self.__validate_parameters()

        init_pair(99, select_color[0], select_color[-1])
        init_pair(98, unselect_color[0], unselect_color[-1])

    def select(self) -> Union[str, int, object]:
        """
        使用getch开始监听键盘操作，选择选项
        :return: 无
        """
        self.panel.top()
        update_panels()
        doupdate()  # 将面板移动至最上，并刷新
        self.__validate_screen()
        now = 0
        max_index = len(self.menu.items()) - 1
        menu = list(self.menu.items())
        while True:
            for i in range(len(menu)):  # 插入菜单选项
                if now == i:
                    self.__add_str(menu[i][-1], True)
                else:
                    self.__add_str(menu[i][-1])
                self.win.addch('\n')
            self.win.refresh()
            key = self.win.getkey()  # 按键侦测
            if key == "KEY_UP":
                if now > 0:
                    now -= 1
            elif key == "KEY_DOWN":
                if now < max_index:
                    now += 1
            elif key == "\n":
                return menu[now][0]
            self.win.clear()

    def change_menu(self, newmenu: dict) -> None:
        """
        更改菜单内容。

          newmenu
            标准同定义该class时的要求。
          :return: 无
        """
        self.menu = newmenu
        self.__validate_parameters()

    def change_color(self, select_color: Tuple[int, int], unselect_color: Tuple[int, int]) -> None:
        """
        更改颜色配置。

          select_color
            被选中时显示的颜色。要求同定义该class时一样。缺省请使用<instance>.select_color。
          unselect_color
            为选中时显示的颜色。要求同定义该class时一样。缺省请使用<instance>.unselect_color。
          :return: 无
        """
        self.select_color = select_color
        self.unselect_color = unselect_color
        self.__validate_parameters()

    def __validate_parameters(self):
        """
        验证所有参数是否符合类型，避免之后出现错误
        :return: 无
        """
        typee = "type mismatched"
        lengthe = "invalid length/count"
        assert isinstance(self.menu, dict), typee
        assert len(self.menu) > 0, lengthe
        assert isinstance(self.win, window), typee
        assert isinstance(self.prefix, str), typee
        assert isinstance(self.style, str), typee
        assert isinstance(self.align, bool), typee
        assert isinstance(self.select_color, tuple), typee
        assert isinstance(self.unselect_color, tuple), typee
        assert len(self.select_color) == 2 or len(self.unselect_color) == 2, lengthe

    def __add_str(self, content: str, contrast: bool = False) -> None:
        """
        向window添加字符串，进行颜色处理，使用self.select_color以及self.unselect_color的设置。

          content
            接受一个字符串，要向window添加的字符串。
          contrast
            接受一个布尔值，是否进行突出显示。
          :return: 无
        """
        padding = " " * len(self.prefix) if self.align else ""
        if contrast:  # 选中选项字符处理
            self.win.attron(color_pair(99))
            if self.style == "CONTRAST":
                self.win.addstr(content, A_STANDOUT)
            elif self.style == "PREFIX":
                self.win.addstr(self.prefix+content)
            elif self.style == "COLOR":
                self.win.addstr(content)
            return self.win.attroff(color_pair(99))
        self.win.attron(color_pair(98))  # 普通字符处理
        if self.style == "CONTRAST":
            self.win.addstr(content)
        else:
            self.win.addstr(padding+content)
        return self.win.attroff(color_pair(98))

    def __validate_screen(self) -> None:
        rows = len(self.menu.items())
        columns = max(map(len, self.menu.values()))
        if self.max_rows < rows or self.max_columns < columns:
            raise WindowSizeError("window size too small")


class WindowSizeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
