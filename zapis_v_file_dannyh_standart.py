file_obj = open('100_xodov7.txt', 'a')
for i in range(400):
 chislo =random.randint(0,36) # генерируем число
 file_obj.write(str(chislo)+'\n')

file_obj.close()