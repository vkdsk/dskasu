import time
import win32gui
import win32con
import win32api

# Получить список всех видимых окон
def get_visible_windows():
    hwnds = []
    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
    win32gui.EnumWindows(enum_handler, None)
    return set(hwnds)

print("Запоминаю окна...")
known_windows = get_visible_windows()
print("Ожидание появления нового окна...")

while True:
    time.sleep(10)  # Проверка раз в 10 секунд
    current_windows = get_visible_windows()
    new_windows = current_windows - known_windows

    if new_windows:
        hwnd = new_windows.pop()
        title = win32gui.GetWindowText(hwnd)
        print(f"Найдено новое окно: {title}")

        # Разворачиваем окно на случай, если оно свернуто
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        # Alt-хак, чтобы обойти защиту SetForegroundWindow
        win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Нажатие Alt
        win32gui.SetForegroundWindow(hwnd)              # Активация окна
        win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)  # Отпускание Alt

        time.sleep(0.5)

        # Два раза Enter
        for _ in range(2):
            win32api.keybd_event(0x0D, 0, 0, 0)  # VK_RETURN (Enter down)
            time.sleep(0.1)
            win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)  # VK_RETURN (Enter up)
            time.sleep(0.3)

        print("Окно активировано и Enter нажаты дважды. Завершение.")
        break