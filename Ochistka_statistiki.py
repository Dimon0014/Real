import json
import win32api, win32con, time

# with open('real_01_ochistka.txt', 'r') as f:  # извлекаем  из файла
#     data2 = json.load(f)
# print(data2)
                                    ##

viborka = []                                          ##
file_obj = open('29cikl.txt')                      ## Создание списка из нагерерированого
data_list = file_obj.readlines()                      ##
i = 0
for line in data_list:                                ##
    i = i + 1
    if i%2 ==0:
        viborka.append(int(line))
file_obj.close()
print(viborka)


file_obj = open('29cikl_och.txt', 'w')
file_obj.writelines("%s\n" % i for i in viborka)
# for item in viborka:
#    file_obj.writeline(str(item)+'/n')
# file_obj.close()