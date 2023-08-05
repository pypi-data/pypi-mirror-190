import win32gui
import win32con
class WindowsPoint:

    def __init__(self):
        self.windowList = []
        self.content = "content"
        self.hwnd = -1

    def _getWindowList(self):
        """清空原来的列表"""
        win32gui.EnumWindows(self._enumWindows, None)

    def _enumWindows(self, hwnd, _):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            phwnd = win32gui.GetParent(hwnd)
            title = win32gui.GetWindowText(hwnd)
            name = win32gui.GetClassName(hwnd)

            if self.hwnd != -1:
                return

            self.hwnd = hwnd
            for content in self.contents:
                if content not in name and content not in title:
                    self.hwnd = -1


    def get_hwnd(self, contents):
        self.contents = contents
        self._getWindowList()
        return self.hwnd


    def focus_windows(self,hwnd):

        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        else:
            print(hwnd)
            win32gui.SetForegroundWindow(hwnd)





# win32gui.SetForegroundWindow(527916)