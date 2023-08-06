import ddtank



def get_game_window_handle() -> list:
    """
    获取所有游戏窗口句柄
    :return: 由游戏窗口句柄组成的列表
    """
    hwnd_title = dict()
    hwnd_list = list()

    def get_all_hwnd(hwnd, mouse):
        if ddtank.win32gui.IsWindow(hwnd) and ddtank.win32gui.IsWindowEnabled(hwnd) and ddtank.win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: ddtank.win32gui.GetWindowText(hwnd)})

    ddtank.win32gui.EnumWindows(get_all_hwnd, 0)

    for h, t in hwnd_title.items():
        if '彈彈堂' in t:
            hwnd_list.append(h)
    return hwnd_list

