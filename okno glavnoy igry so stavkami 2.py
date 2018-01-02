import wx, sys
import json
import random
import  psutil
import subprocess
import win32api, win32gui, win32con, time
from datetime import datetime, timedelta
from time import clock
class MyApp(wx.App): # создаем класс оконной программы
  def OnInit(self): # инициализация программы
      self.frame = MyFrame(None, title="The Main Frame") # создание фрейма на основе нашего класса MyFrame2
      self.SetTopWindow(self.frame) #устанавливаем окно программы сверху остальных окон
      self.frame.Show() # показываем окно
      return True
class MyFrame(wx.Frame):
   def __init__(self, parent, id=wx.ID_ANY, title="frame",
                pos=wx.DefaultPosition, size=wx.DefaultSize,
                style=wx.DEFAULT_FRAME_STYLE,
                name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title,
        pos, size, style, name)
        # Attributes
        #style = wx.TRANSPARENT_WINDOW if sys.platform.lower() == 'win32' else 0
        self.x_pad = 0
        self.y_pad = 0
        self.schet_gig_cikl=0

        self.panel = wx.Panel(self, -1, style=wx.TRANSPARENT_WINDOW)
        self.btn1 = wx.Button(self.panel, label="Push Me")
        self.btn2 = wx.Button(self.panel, label="push me too")
        #self.SetTransparent(80)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.btn1, 0, wx.ALIGN_RIGHT, 10)
        sizer.Add(self.btn2, 0, wx.ALIGN_RIGHT, 10)
        self.panel.SetSizer(sizer)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn1)
        self.Bind(wx.EVT_BUTTON,                          #ВТОРАЯ КНОПКА ДЕЛАЕТ ПЕРВУЮ ЛИБО АКТИВНОЙ ЛИБО НЕДОСТУПНОЙ(СЕРОЙ)
                  lambda event:                           # функция выполнения прописана через лямбду функцию, которой
                  self.btn1.Enable(not self.btn1.Enabled),# передается событие event
                  self.btn2)       # хитрая конструкция not self.btn1.Enabled, переворачивает
                                   # результат 'self.btn1.Enabled' типа если True возращает False, если False возращает True

   def ScreenShotChisla(self,coordinaty):
       """
       Делает скриншот выбранного фрагмента экрана
       Основано на методе, предложенном Андреа Гавана
       """

       with open(coordinaty, 'r') as f:  # извлекаем  из файла
           data2 = json.load(f)
       #print('', data2)
       rect1 = data2
       #print('rect', rect1)

       rect = self.GetRect()  # получаем координаты своего окна
       rect.x = rect1[0]  # +134
       rect.y = rect1[1]  # +275
       rect.width = rect1[2] - rect1[0]  # +1080)
       rect.height = rect1[3] - rect1[1]  # +691)
       # print('координаты', rect.x, rect.y, rect.width, rect.height)
       # Настройка ширины для Linux обнаружено Джоном Торресом
       # http://article.gmane.org/gmane.comp.python.wxpython/67327
       if sys.platform == 'linux2':
           client_x, client_y = self.ClientToScreen((0, 0))
           border_width = client_x - rect.x
           title_bar_height = client_y - rect.y
           rect.width += (border_width * 2)
           rect.height += title_bar_height + border_width

       # Сделать скриншот всей зоны DC (контекста устройства)
       dcScreen = wx.ScreenDC()

       # Создать битмап, в котором сохранится скриншот
       # Учтите, что битмап должен быть достаточно большим, чтобы в него поместился скриншот
       # -1 значит использование текущей стандартной глубины цвета
       bmp = wx.Bitmap(rect.width, rect.height)

       # # Создать в памяти DC, который будет использован непосредственно для скриншота
       memDC = wx.MemoryDC()
       #
       # # Прикажите DC использовать наш битмап
       # # Все изображения из DC теперь переместится в битмап
       memDC.SelectObject(bmp)
       #
       # # Blit в данном случае скопируйте сам экран в кэш памяти
       # # и, таким образом, он попадёт в битмап
       # Blit  копирует битовые блоки из одного контекста в другое
       # в дданном случае у нас есть контекст всего экрана в переменной dcScreen
       # а также мы создали контекст в памяти memDC, после чего инициализировали(memDC.SelectObject(bmp))
       # его пустым объектом Bitmap
       # который храниться в переменной bmp(таким образом просто задали размер памяти который ножен для хранения
       # битовой матрицы (контекста))
       # после чего через функцию Blit копируем битовые блоки из dcScreen
       memDC.Blit(0,  # Скопируйте сюда координат Х
                  0,  # Скопируйте сюда координат Y
                  rect.width,  # Скопируйте эту ширину
                  rect.height,  # Скопируйте эту высоту
                  dcScreen,  # Место, откуда нужно скопировать
                  rect.x,  # Какой офсет у Х в оригинальном DC (контексте устройства из которого копируем(в данном
                  # случае у dcScreen ) то есть копируем не весь экран а часть)
                  rect.y  # Какой офсет у Y в оригинальном DC
                  )

       # # Select the Bitmap out of the memory DC by selecting a new
       # # uninitialized Bitmap
       memDC.SelectObject(wx.NullBitmap)  # освобождаем память от битмапа, прежде чем снова ее задействовать
       # освобождение будет автоматическим если больше не буде обращения к
       #  объекту  wx.MemoryDC. То есть освобождать надо если планируем еще
       #  использовать для другой картинки. В данном случае можно и не освобождать

       img = bmp.ConvertToImage()  # конвертация в изображение которое можно вывести на экран
       return img
   def onPlacewindow(self, name):
       # """



       toplist, winlist = [], []  # пустые списки куда будут запихиваться хандлы окон                      #европейская рулетка премиум - william hill casino
       nameWindow = name

       def enum_cb(hwnd, results):
           winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

       win32gui.EnumWindows(enum_cb, toplist)
       print(winlist)
       windowToInterest = [(hwnd, title) for hwnd, title in winlist if
                           nameWindow in title.lower()]  # получение хендла по title
       # just grab the hwnd for first window matching firefox
       print(len(windowToInterest))
       # if len(firefox1)==1:
       hwnd1 = windowToInterest
       print(repr(hwnd1))
       firefox = windowToInterest[0]  # мы тут отсекли название окна
       hwnd = firefox[0]
       print(repr(hwnd))
       # y = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN) # получаем координату Y(начало в данном случае Y=0)
       win32gui.SetForegroundWindow(hwnd)  # выводит на передний план окно

       # win32gui.SetWindowPlacement(hwnd,(0, 1, (-1, -1), (-1, -1), (1922, 0, 2720, 474)))

       with open('WindowPlace.txt', 'r') as f:  # извлекаем  из файла
        place = json.load(f)

       win32gui.SetWindowPlacement(hwnd, place)
   def leftClick(self):
       win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
       time.sleep(.1)
       win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
       #print("Click.")  # completely optional. But nice for debugging purposes.

   def mousePos(self,cord):
       win32api.SetCursorPos((self.x_pad + cord[0], self.y_pad + cord[1]))
       time.sleep(0.1)
       self.leftClick()


   def initial_x_y(self):
       with open('xy_coord.txt', 'r') as f:  # извлекаем  из файла
           data2 = json.load(f)

       self.data_fin2 = []

       for item in data2:  # приводим к типу Python
           self.data_fin2.append(list(item))

       with open('xy_coord2.txt', 'r') as f:  # извлекаем  из файла
           data4 = json.load(f)

       self.data_vhod4 = []
       for item in data4:  # приводим к типу Python
           self.data_vhod4.append(list(item))

       # print('список координат x y', self.data_fin2)  # проверка готового результата
       # # все первые индексы отражают имя координаты
       #print(self.data_fin2[0][0]) #icon
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
       return self.data_fin2

   def initial_x_y2(self):


       with open('xy_coord2.txt', 'r') as f:  # извлекаем  из файла
           data4 = json.load(f)

       self.data_vhod4 = []
       for item in data4:  # приводим к типу Python
           self.data_vhod4.append(list(item))

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
       return self.data_vhod4

   def initial_pic(self):
      pic=[]
      for i in range(38):
           name = str(i)+'.bmp'
           name = wx.Image(name, type=wx.BITMAP_TYPE_ANY)
           pic.append(name)
      return   pic
   def vremja_str(self):

       now = datetime.now()
       now = now + timedelta(hours=0)
       tme = now.strftime("%d,%m,%y %H.%M.%S")  # %d,%m,%y
       # now = now + timedelta(hours=0)
       return tme
######################## отсюда и до главной  функции ставки и предсказания
   def last_last_seen_steps_of_simv_01(self, dict, key):  # альтернатива  "last_next_seen_all_steps_1"
       result = dict[key][0]

       # print('функия next_seen_steps =',result)
       return result

   def dob_next_seen_1(self,dict, key, steps):  # функция добавления/инициализация шагов с последнего появления

       if (key) in dict:  # проверка на наличие значений
           last_seen = self.last_last_seen_steps_of_simv_01(dict, key)
           # print('steps-last_time seen_in_key =', last_seen)
           # print('печатает dict[key][1][0]', dict[key][1][0])
           dict[key][1].append(last_seen)
           dict[key][2] = len(dict[key][1])  # сколько раз уже выпадала


       else:  # инициализация
           dict.update({(key): [0, [steps], 1, key, steps]})  # инициализация
           # print('key in function =', key)

   def add_step_to_all_1(self,dict):
       for item in dict:
           dict[item][0] = dict[item][0] + 1
           dict[item][4] = dict[item][4] + 1

   def pre1_predskazatel_1(self,key, list_of200, steps_of_predscazan):
       keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
               29, 30, 31, 32, 33, 34, 35, 36]
       list = list_of200

       for item in keys:
           if item == key:
               list.append(key)
               if len(list) > steps_of_predscazan:
                   list.pop(0)
       return list

   def pre2_predskazatel_1(self,list_of200):
       keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
               29, 30, 31, 32, 33, 34, 35, 36]
       list = list_of200
       list_par = []
       for item in keys:
           list_par.append([item, 0])
           for it in list:
               if it == item:
                   list_par[item][1] = list_par[item][1] + 1
       return list_par
       # for it in keys:
       #     for item in list:
       #         if item not in d:
       #             list_par.append([item])
       #         else:
       #             d[c] += 1

   def pre3_predskazatel_1(self,list_sort):

       list_sort.sort(key=lambda item: item[1])
       list_sort.reverse()
       # nolik = list_sort[0][0]
       # odin = list_sort[1][0]
       # dva = list_sort[2][0]
       # #tri = list_sort[3][0]
       # result =list_sort[0][0] # random.choice([nolik,odin,dva] )
       if list_sort[0][1] > 1:
           result = list_sort[0][0]  # random.choice([nolik,odin,dva] )
       else:
           result = 99
       return result

   def proverka_predskaza_1(self,key, list_of_win_proverki, winer_1, steps):
       if key == list_of_win_proverki[2]:
           # print('pered append', list_of_win_proverki_1[2])
           #list_of_all_Win_1.append(list_of_win_proverki[2])
           # print('steps',steps,' vyigral key ', key, list_of_win_proverki[2])
           list_of_win_proverki[1] = 1
           result = list_of_win_proverki  # первое значение - количество шагов
           # второе значени флаг сброса продолжения проверки перестать - еденица 1, продолжить ноль 0
           # третье значение предсказаное число
       else:
           list_of_win_proverki[1] = 0

           list_of_win_proverki[0] = list_of_win_proverki[0] + 1

           result = list_of_win_proverki

       # if winer_1 == 99:
       #     #list_of_win_proverki[0] = list_of_win_proverki[0] - 1 # зачем уменьшать количество шагов, все правильно мы же подрят все шаги считаем
       #     result = list_of_win_proverki
       return result

   def Glavnaja(self):
       start1 = clock()
       vhod=True
       cikl_of_start =0
       file_obj2 = open('chet01.txt', 'a')
       file_obj3 = open('log.txt', 'a')
       dataMouse = self.initial_x_y()
       dataMouse2 = self.initial_x_y2()
       dataPic = self.initial_pic()

       # print[dataPic]

       # self.leftClick()

       while (vhod):
           sttepers =0
           list_of_win_proverki_1 = [0, 0, -1, 0, 0, 0, 0]
           steps_to_win_1 = 0
           list_of200_1 = []
           list_par_of200_1 = []
           list_of_win200_1 = []
           chislo_of = 99
           winer_1 = 99
           dic_ed = {}  # болванка под словарь едениц
           list_of_steps_toWin_1 = []
           cikl_of_start = cikl_of_start+1
           now_name = datetime.now()
           tme_name = now_name.strftime("%d,%m,%y %H.%M.%S")
           name_of_file_real = 'poputka_'+str(cikl_of_start)+'_data'+tme_name+'.txt'
           file_obj = open(name_of_file_real, 'a')
           time.sleep(0.5)
           self.schet_gig_cikl += 1
           PROCNAME = 'casino.exe'
           for proc in psutil.process_iter():
               try:
                   if proc.name() == PROCNAME:
                       p = psutil.Process(proc.pid)
                       print('psutil', p.username())
                       time.sleep(2)
                       #game.terminate()
                       proc.kill()
                       time.sleep(7)
                       print('psutil_ubil_process')
               except:
                   print('psutil_oshibka')
                   pass
           time.sleep(3)
           game = subprocess.Popen(["C:\Program Files (x86)\William Hill Casino\casino.exe"], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
           time.sleep(80)
           screen = self.ScreenShotChisla('coord_snapshot_vhoda.txt')
           tme = self.vremja_str()
           name_screen_log1 = 'screen_log1'+tme+'.bmp'
           screen.SaveFile(name_screen_log1, wx.BITMAP_TYPE_BMP)
           time.sleep(12)

           screen1 = self.ScreenShotChisla('coord_snapshot_vhoda2.txt')
           name_screen1_log2 = 'screen_log2' + tme + '.bmp'
           screen1.SaveFile(name_screen1_log2, wx.BITMAP_TYPE_BMP)
           vhod1 = wx.Image('vhod0.bmp', type=wx.BITMAP_TYPE_ANY) # произошла ошибка
           vhod2 = wx.Image('vhod1.bmp', type=wx.BITMAP_TYPE_ANY) # завис на загрузке
           vhod3 = wx.Image('vhod.bmp', type=wx.BITMAP_TYPE_ANY) # успешный вход
           vhod4 = wx.Image('vhod2.bmp', type=wx.BITMAP_TYPE_ANY) # вообще не загрузился


           p = screen.GetData()
           p1 = screen1.GetData()
           p_2 = vhod1.GetData()
           p3 = vhod2.GetData()
           p4= vhod3.GetData()
           p5 =vhod4.GetData()
           if p5 == p:
               time.sleep(1)
               tme = self.vremja_str()
               file_obj3.write('terminate process' + tme + '\n')
               time.sleep(1)
               game.terminate()
               time.sleep(600)
               continue
           if p_2  == p:
               print('proizoshla oshibka')
               tme = self.vremja_str()
               file_obj3.write('Ne udalos voyti poizoshla oshibka' + tme + '\n')
               time.sleep(5)
               time.sleep(1)
               game.terminate()
               time.sleep(3720)
               continue
           if p3 == p:
               print('zavis pri zagruzke')
               tme = self.vremja_str()
               file_obj3.write('Ne udalos voyti zavis pri zagruzke' + tme + '\n')
               time.sleep(5)
               time.sleep(1)
               game.terminate()
               time.sleep(3720)
               continue

           if  p4 == p1:
               time.sleep(1)
               self.mousePos(dataMouse[1][1])
               time.sleep(12)
               tme = self.vremja_str()
               screen3 = self.ScreenShotChisla('coord_snapshot_vhoda.txt')
               name_screen3_log3 = 'screen3_log3' + tme + '.bmp'
               screen3.SaveFile(name_screen3_log3, wx.BITMAP_TYPE_BMP)
               vhod10 = wx.Image('vhod_3.bmp', type=wx.BITMAP_TYPE_ANY)
               p00 = screen3.GetData()
               p10 = vhod10.GetData()
               time.sleep(1)
               if p00 == p10:
                   time.sleep(1)
                   self.mousePos(dataMouse2[0][1])
                   time.sleep(1)
                   self.mousePos(dataMouse2[1][1])
                   # time.sleep(1)
                   # self.mousePos(dataMouse[1][1])
              # vhod = False
                   file_obj3.write('Vhod proshel uspeshno 1 ' + tme + '\n')
               else:

                 file_obj3.write('Vhod proshel uspeshno 2 ' + tme + '\n')

               break
       file_obj3.close()
       time.sleep(10)
       try:
           self.onPlacewindow("европейская рулетка премиум - william hill casino")
           time.sleep(10)
           self.mousePos(dataMouse[2][1])
           self.leftClick()
       except:
           print('okno kuda to podevalos_oshibka')
           game.terminate()
           time.sleep(40)
           self.Glavnaja()
           #pass
       steps = 0
       seconds = 0
       chet =0
       chicloVrach = random.randint(395, 443)
       while ( steps < chicloVrach):
           screen_control_2 = self.ScreenShotChisla('coord_snapshot_control.txt')
           p_cntr_2 = screen_control_2.GetData()
           chicloVrach = random.randint(395, 443)
           start = clock()
           first0 = time.time()
           steps = steps + 1
           file_obj.write('n xoda' + str(steps) + '\n')
           steps_vnutri_pervogo_cikla = 0
           while (True):
               time.sleep(1.5)
               steps_vnutri_pervogo_cikla = steps_vnutri_pervogo_cikla + 1
               screen = self.ScreenShotChisla('coord_snapshot.txt')
               p = screen.GetData()
               p2 = dataPic[37].GetData()
               if p == p2:
                   time.sleep(0.05)
                   #print("есть вращение")
                   # prod_cikla = False
                   break
               else:
                   # time.sleep(0.1)
                   self.mousePos(dataMouse[2][1])
                   break
           steps_vnutri_vtorogo_cikla = 0
           steps_vnutri =0
           while (True):
               time.sleep(0.8)
               steps_vnutri_vtorogo_cikla = steps_vnutri_vtorogo_cikla + 1
               screen_control_1 = self.ScreenShotChisla('coord_snapshot_control.txt')
               time.sleep(0.1)
               screen5 = self.ScreenShotChisla('coord_snapshot.txt')
               p = screen5.GetData()
               p_cntr_1 = screen_control_1.GetData()

               #p2 = dataPic[37].GetData()
               if p_cntr_1 == p_cntr_2:
                   print("вращение не закончилось")
                   # prod_cikla = False
                   steps_vnutri = steps_vnutri+1
                   if steps_vnutri == 9:
                       self.mousePos(dataMouse[2][1])
                       self.leftClick()
                       print("dopolnitelnyi click")

                   if steps_vnutri == 20:
                       self.mousePos(dataMouse[2][1])
                       self.leftClick()
                       print("dopolnitelnyi click2")
                   continue
               else:
                   # chislo=True
                   steps_vnutri =0
                   for i in range(len(dataPic)):
                       prod_cikla = True
                       # p = screen.GetData()
                       time.sleep(0.01)
                       p2 = dataPic[i].GetData()
                       if p == p2:
                           print("выпал номер", i)
                           chislo_of =i
                           #time.sleep(0.05)
                           file_obj.write(str(i) + '\n')
                           time.sleep(0.05)
                           # chislo = False
                           prod_cikla = False

                           screen_control_2 = self.ScreenShotChisla('coord_snapshot_control.txt')
                           p_cntr_2 = screen_control_2.GetData()

                   #################################################################################
                   ##             здесь мы узнаем число   и начинаем действовать
                   key1 = chislo_of
                   print('key1:', key1)
                   if winer_1 != 99:  # если предсказания нет то и играть не будем
                       sttepers = sttepers + 1
                       print('steps:', steps, 'v igre')
                       print('sttepers:', sttepers)

                       list_of_win_proverki_1 = self.proverka_predskaza_1(key1, list_of_win_proverki_1, winer_1, steps)


                       # if list_of_win_proverki_1_0[1] == 1:
                       #     list_of_win_1_0_all.append(list_of_win_proverki_1_0[2])
                       if list_of_win_proverki_1[1] == 1:  # если предсказание сбросило активность то назначаем новую цифру выиграша
                           sttepers = 1

                           #list_of_win_proverki_1_0[7].append(list_of_win_proverki_1_0[2])
                           steps_to_win_1 = list_of_win_proverki_1[
                               0]  # забираем в буферную переменную количество шагов до выигрыша
                           # print('list_of_win_proverki_1[2]', list_of_win_proverki_1[2])
                           print('key                       ', key1)
                           #print('steps', steps, 'steps_to_win_1:', steps_to_win_1, ': list_of_win__1[2]', stat_02,'winer_1', winer_1)


                           list_of_win_proverki_1[2] = winer_1  # назначение нового числа предсказания _ назначение с опаздыванием на один шаг
                           list_of_steps_toWin_1.append(steps_to_win_1)
                           list_of_win_proverki_1[0] = 1  # обнуляем количество шагов до выигрыша
                           # list_of_win_proverki_1[4] = list_of_win_proverki_1[4]+ 35
                           # list_of_win_proverki_1[5] = 1
                           # print(dic_ed[(key)] )
                       if list_of_win_proverki_1[0] > 54:
                           list_of_steps_toWin_1.append(60)
                           list_of_win_proverki_1[0] = 1
                           list_of_win_proverki_1[1] = 0
                           sttepers =1
                           # list_of_win_proverki_1[0] = list_of_win_proverki_1[0] + 1

                           # list_of_win_proverki_1[2] = winer_1 # назначение нового числа предсказания _ назначение с опаздыванием на один шаг
                        # типа здесь делаем ставки на то число которое в list_of_win_proverki_1[2]
                       if sttepers <37:# шагов меньше 36 ставим ставку
                           self.mousePos(dataMouse[3][1]) # минимальная ставка
                           time.sleep(0.05)
                           if  list_of_win_proverki_1[2] ==0:
                              self.mousePos(dataMouse[8][1]) # ставка на число 0
                              print('stavka na chislo: 0')
                           if  list_of_win_proverki_1[2] ==1:
                              self.mousePos(dataMouse[9][1]) # ставка на число 1
                              print('stavka na chislo: 1')
                           if list_of_win_proverki_1[2] == 2:
                               self.mousePos(dataMouse[10][1])  # ставка на число 2
                               print('stavka na chislo: 2')
                           if list_of_win_proverki_1[2] == 3:
                               self.mousePos(dataMouse[11][1])  # ставка на число 3
                               print('stavka na chislo: 3')
                           if list_of_win_proverki_1[2] == 4:
                               self.mousePos(dataMouse[12][1])  # ставка на число 4
                               print('stavka na chislo: 4')
                           if list_of_win_proverki_1[2] == 5:
                               self.mousePos(dataMouse[13][1])  # ставка на число 5
                               print('stavka na chislo: 5')
                           if list_of_win_proverki_1[2] == 6:
                               self.mousePos(dataMouse[14][1])  # ставка на число 6
                               print('stavka na chislo: 6')
                           if list_of_win_proverki_1[2] == 7:
                               self.mousePos(dataMouse[15][1])  # ставка на число 7
                               print('stavka na chislo: 7')
                           if list_of_win_proverki_1[2] == 8:
                               self.mousePos(dataMouse[16][1])  # ставка на число 8
                               print('stavka na chislo: 8')
                           if list_of_win_proverki_1[2] == 9:
                               self.mousePos(dataMouse[17][1])  # ставка на число 9
                               print('stavka na chislo: 9')
                           if list_of_win_proverki_1[2] == 10:
                               self.mousePos(dataMouse[18][1])  # ставка на число 10
                               print('stavka na chislo: 10')
                           if list_of_win_proverki_1[2] == 11:
                               self.mousePos(dataMouse[19][1])  # ставка на число 11
                               print('stavka na chislo: 11')
                           if list_of_win_proverki_1[2] == 12:
                               self.mousePos(dataMouse[20][1])  # ставка на число 12
                               print('stavka na chislo: 12')
                           if list_of_win_proverki_1[2] == 13:
                               self.mousePos(dataMouse[21][1])  # ставка на число 13
                               print('stavka na chislo: 13')
                           if list_of_win_proverki_1[2] == 14:
                               self.mousePos(dataMouse[22][1])  # ставка на число 14
                               print('stavka na chislo: 14')
                           if list_of_win_proverki_1[2] == 15:
                               self.mousePos(dataMouse[23][1])  # ставка на число 15
                               print('stavka na chislo: 15')
                           if list_of_win_proverki_1[2] == 16:
                               self.mousePos(dataMouse[24][1])  # ставка на число 16
                               print('stavka na chislo: 16')
                           if list_of_win_proverki_1[2] == 17:
                               self.mousePos(dataMouse[25][1])  # ставка на число 17
                               print('stavka na chislo: 17')
                           if list_of_win_proverki_1[2] == 18:
                               self.mousePos(dataMouse[26][1])  # ставка на число 18
                               print('stavka na chislo: 18')
                           if list_of_win_proverki_1[2] == 19:
                               self.mousePos(dataMouse[27][1])  # ставка на число 19
                               print('stavka na chislo: 19')
                           if list_of_win_proverki_1[2] == 20:
                               self.mousePos(dataMouse[28][1])  # ставка на число 20
                               print('stavka na chislo: 20')
                           if list_of_win_proverki_1[2] == 21:
                               self.mousePos(dataMouse[29][1])  # ставка на число 21
                               print('stavka na chislo: 21')
                           if list_of_win_proverki_1[2] == 22:
                               self.mousePos(dataMouse[30][1])  # ставка на число 22
                               print('stavka na chislo: 22')
                           if list_of_win_proverki_1[2] == 23:
                               self.mousePos(dataMouse[31][1])  # ставка на число 23
                               print('stavka na chislo: 23')
                           if list_of_win_proverki_1[2] == 24:
                               self.mousePos(dataMouse[32][1])  # ставка на число 24
                               print('stavka na chislo: 24')
                           if list_of_win_proverki_1[2] == 25:
                               self.mousePos(dataMouse[33][1])  # ставка на число 25
                               print('stavka na chislo: 25')
                           if list_of_win_proverki_1[2] == 26:
                               self.mousePos(dataMouse[34][1])  # ставка на число 26
                               print('stavka na chislo: 26')
                           if list_of_win_proverki_1[2] == 27:
                               self.mousePos(dataMouse[35][1])  # ставка на число 27
                               print('stavka na chislo: 27')
                           if list_of_win_proverki_1[2] == 28:
                               self.mousePos(dataMouse[36][1])  # ставка на число 28
                               print('stavka na chislo: 28')
                           if list_of_win_proverki_1[2] == 29:
                               self.mousePos(dataMouse[37][1])  # ставка на число 29
                               print('stavka na chislo: 29')
                           if list_of_win_proverki_1[2] == 30:
                               self.mousePos(dataMouse[38][1])  # ставка на число 30
                               print('stavka na chislo: 30')
                           if list_of_win_proverki_1[2] == 31:
                               self.mousePos(dataMouse[39][1])  # ставка на число 31
                               print('stavka na chislo: 31')
                           if list_of_win_proverki_1[2] == 32:
                               self.mousePos(dataMouse[40][1])  # ставка на число 32
                               print('stavka na chislo: 32')
                           if list_of_win_proverki_1[2] == 33:
                               self.mousePos(dataMouse[41][1])  # ставка на число 33
                               print('stavka na chislo: 33')
                           if list_of_win_proverki_1[2] == 34:
                               self.mousePos(dataMouse[42][1])  # ставка на число 34
                               print('stavka na chislo: 34')
                           if list_of_win_proverki_1[2] == 35:
                               self.mousePos(dataMouse[43][1])  # ставка на число 35
                               print('stavka na chislo: 35')
                           if list_of_win_proverki_1[2] == 36:
                               self.mousePos(dataMouse[44][1])  # ставка на число 36
                               print('stavka na chislo: 36')
                           time.sleep(0.05)
                           self.mousePos(dataMouse[2][1])
                           self.leftClick()
                   #         break
                       else:
                            time.sleep(0.05)
                            self.mousePos(dataMouse2[2][1])
                            time.sleep(0.1)
                            self.leftClick()
                            time.sleep(0.1)
                            self.mousePos(dataMouse[2][1])
                  #         break
                   else:
                        time.sleep(0.05)
                        self.mousePos(dataMouse2[2][1])
                        time.sleep(0.1)
                        self.leftClick()
                        time.sleep(0.1)

                #     # self.mousePos(dataMouse[2][1])
                   #     # self.leftClick()
                   #     break
                   list_of200_1 = self.pre1_predskazatel_1(key1, list_of200_1,8)  # шаг нахождения винера##############################################################

                   list_par_of200_1 = self.pre2_predskazatel_1(list_of200_1)
                   winer_1 = self.pre3_predskazatel_1(list_par_of200_1)
                   if list_of_win_proverki_1[2] == -1:
                       list_of_win_proverki_1[2] = 0



                   #best_chisla = pre3_predskazatel_1_all(list_par_of200_1)
                   ##################################### --- УЧЕТ ЕДЕНИЦ БЛОК НЕ ТРОГАЕМ --- ######################
                   ################################################################################################
                   self.dob_next_seen_1(dic_ed, key1, steps)  # создание\ обновление словаря едениц ###############
                   self.add_step_to_all_1(dic_ed)  # добавление шагов всем еденицам ###############################
                   ################################################################################################
                   break


               print('steps_vnutri_vtorogo_cikla',steps_vnutri_vtorogo_cikla )
               if steps_vnutri_vtorogo_cikla == 40:
                   try:
                       print('steps_vnutri_vtorogo_cikla_doljen byt_click', steps_vnutri_vtorogo_cikla)
                       self.onPlacewindow("европейская рулетка премиум - william hill casino")
                       time.sleep(4)

                       self.mousePos(dataMouse[2][1])
                       self.leftClick()
                   except:
                       print('okno kuda to podevalos_oshibka')
                       pass
               if steps_vnutri_vtorogo_cikla == 55:
                   print('steps_vnutri_vtorogo_cikla_doljen byt_2_y_click', steps_vnutri_vtorogo_cikla)
                   self.mousePos(dataMouse[2][1])
                   self.leftClick()
               if steps_vnutri_vtorogo_cikla == 80:
                   print('steps_vnutri_vtorogo_cikla_doljen byt_2_y_click', steps_vnutri_vtorogo_cikla)
                   self.mousePos(dataMouse[6][1])
                   time.sleep(1)
                   self.mousePos(dataMouse[1][1])
                   time.sleep(9)
                   screen3 = self.ScreenShotChisla('coord_snapshot_vhoda.txt')
                   name_screen3_log3 = 'screen3_log3' + tme + '.bmp'
                   screen3.SaveFile(name_screen3_log3, wx.BITMAP_TYPE_BMP)
                   vhod10 = wx.Image('vhod_3.bmp', type=wx.BITMAP_TYPE_ANY)
                   p00 = screen3.GetData()
                   p10 = vhod10.GetData()
                   time.sleep(1)
                   if p00 == p10:
                       time.sleep(1)
                       self.mousePos(dataMouse2[0][1])
                       time.sleep(1)
                       self.mousePos(dataMouse2[1][1])
                   time.sleep(15)
                   try:
                     self.onPlacewindow("европейская рулетка премиум - william hill casino")
                     time.sleep(10)
                     self.mousePos(dataMouse[2][1])
                     self.leftClick()
                   except:
                       print('okno ne udalos vostanovit to podevalos_oshibka')
                       pass
               # if steps_vnutri_vtorogo_cikla == 29:
               #     print('steps_vnutri_vtorogo_cikla', steps_vnutri_vtorogo_cikla)
               #     self.mousePos(dataMouse[2][1])
               #     self.leftClick()
               if steps_vnutri_vtorogo_cikla>100:
                   game.terminate()
                   time.sleep(5)
                   file_obj3 = open('log.txt', 'a')
                   file_obj3.write('cik igry: '+str(self.schet_gig_cikl)+'Beskonechyi vtoroy cikl ' + tme + '\n')
                   file_obj3.close()
                   file_obj.write('avariynoe zavershenie raboty'  + '\n')
                   file_obj.close()
                   time.sleep(180)
                   self.Glavnaja()
               if not prod_cikla:
                   break
           end1 = clock()
           print('steps', steps, 'Время:', end1 - start)
           first1 = time.time()
           seconds = seconds + (first1 - first0)

           if seconds > 12:
               start10 = clock()
               seconds = 0
               screen = self.ScreenShotChisla('coord_snapshot_prodolj.txt')
               p = screen.GetData()
               prodolji = wx.Image('prodoljenie.bmp', type=wx.BITMAP_TYPE_ANY)
               p2 = prodolji.GetData()
               if p == p2:
                   self.mousePos(dataMouse[45][1])
                   chet = chet+1
                   file_obj2.write(str(chet) + '\n')
               end10 = clock()
               print('проверка на окно продолжения Время выполнения: ', end10 - start10)
           print('cik igry: ',self.schet_gig_cikl)
       end1 = clock()
       promejutok = end1 - start1
       file_obj.write('vremja raboty' + str(promejutok) + '\n')
       file_obj.close()
       file_obj2.close()
       time.sleep(0.6)
       #self.mousePos(dataMouse[6][1])
       time.sleep(0.1)
       # self.mousePos(dataMouse[7][1])
       # time.sleep(1)
       # self.mousePos(dataMouse[46][1])
       game.terminate()
       time.sleep(1097)
       if self.schet_gig_cikl <11:
           self.Glavnaja()
   def OnButton(self, event):
        """Called when self.btn1 is clicked"""
        self.Glavnaja()
if __name__ == "__main__":
 app = MyApp(False)
 app.MainLoop()