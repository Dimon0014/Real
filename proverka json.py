import json
def initial_x_y():
    with open('xy_coord.txt', 'r') as f:  # извлекаем  из файла
        data2 = json.load(f)

    data_fin2 = []

    for item in data2:  # приводим к типу Python
        data_fin2.append(list(item))

    with open('xy_coord2.txt', 'r') as f:  # извлекаем  из файла
        data4 = json.load(f)

    data_vhod4 = []
    for item in data4:  # приводим к типу Python
        data_vhod4.append(list(item))

    # print('список координат x y', self.data_fin2)  # проверка готового результата
    # # все первые индексы отражают имя координаты
    # print(self.data_fin2[0][0]) #icon
    # print(self.data_fin2[1][0]) #table
    # print(self.data_fin2[2][0]) #start
    # # все следущие индексы выдают список  координат
    # print(self.data_fin2[0][1])  # [291, 207]
    # print(self.data_fin2[1][1])  # [163, 195]
    # print(self.data_fin2[2][1])  # [242, 252]
    # # следущий третий индекс выдает по отдельности x и y  координат
    # print(self.data_fin2[0][1][0])  # x=291
    # print(self.data_fin2[1][1][0])  # x=163
    # print(self.data_fin2[2][1][1])  # y=252
    return data_fin2


# def initial_x_y2():
#     with open('xy_coord2.txt', 'r') as f:  # извлекаем  из файла
#         data4 = json.load(f)
#
#     self.data_vhod4 = []
#     for item in data4:  # приводим к типу Python
#         data_vhod4.append(list(item))
#
#     # print('список координат x y', self.data_fin2)  # проверка готового результата
#     # # все первые индексы отражают имя координаты
#     # print(self.data_fin2[0][0]) #icon
#     # print(self.data_fin2[1][0]) #table
#     # print(self.data_fin2[2][0]) #start
#     # # все следущие индексы выдают список  координат
#     # print(self.data_fin2[0][1])  # [291, 207]
#     # print(self.data_fin2[1][1])  # [163, 195]
#     # print(self.data_fin2[2][1])  # [242, 252]
#     # # следущий третий индекс выдает по отдельности x и y  координат
#     # print(self.data_fin2[0][1][0])  # x=291
#     # print(self.data_fin2[1][1][0])  # x=163
#     # print(self.data_fin2[2][1][1])  # y=252
#     return data_vhod4
t = initial_x_y()
# d = initial_x_y2()
print(t)
# print(d)