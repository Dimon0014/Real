import json
import win32api, win32con, time

with open('xy_coord.txt', 'r') as f:  # извлекаем  из файла
    data2 = json.load(f)

data_fin2 = []
i = 0
for item in data2:  # приводим к типу Python
    data_fin2.append(list(item))

print('список координат x y', data_fin2)  # проверка готового результата
# все первые индексы отражают имя координаты
print(data_fin2[0][0])
print(data_fin2[1][0])
print(data_fin2[2][0])
# все следущие индексы выдают список  координат
print(data_fin2[0][1])  # [291, 207]
print(data_fin2[1][1])  # [163, 195]
print(data_fin2[2][1])  # [242, 252]
# следущий третий индекс выдает по отдельности x и y  координат
print(data_fin2[0][1][0])  # x=291
print(data_fin2[1][1][0])  # x=163
print(data_fin2[2][1][1])  # y=252

x_pad = 0
y_pad = 0


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    print("Click.")  # completely optional. But nice for debugging purposes.

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))