import wx, sys
import json
import random
import pyautogui
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

       with open('xy_coord_2.txt', 'r') as f:  # извлекаем  из файла
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


       with open('xy_coord_2.txt', 'r') as f:  # извлекаем  из файла
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
       nomer_txt_fila = 900
       # self.leftClick()

       while (vhod):
           cikl_of_start = cikl_of_start+1
           nomer_txt_fila = nomer_txt_fila+cikl_of_start
           now_name = datetime.now()
           tme_name = now_name.strftime("%d,%m,%y %H.%M.%S")
           name_of_file_real = str(nomer_txt_fila)+'cikl_'+str(cikl_of_start)+'_data'+tme_name+'.txt'
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
           time.sleep(120)
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
               time.sleep(320)
               continue
           if p3 == p:
               print('zavis pri zagruzke')
               tme = self.vremja_str()
               file_obj3.write('Ne udalos voyti zavis pri zagruzke' + tme + '\n')
               time.sleep(5)
               time.sleep(1)
               game.terminate()
               time.sleep(320)
               continue

           if  p4 == p1:
               time.sleep(1)
               self.mousePos(dataMouse2[3][1]) # клик по окну поиска
               time.sleep(2)
               # здесь вводиться строка поиска penny
               VK_CODE = {'backspace': 0x08, # VK - Virtual Keystroke
                          'tab': 0x09,
                          'clear': 0x0C,
                          'enter': 0x0D,
                          'shift': 0x10,
                          'ctrl': 0x11,
                          'alt': 0x12,
                          'pause': 0x13,
                          'caps_lock': 0x14,
                          'esc': 0x1B,
                          'spacebar': 0x20,
                          'page_up': 0x21,
                          'page_down': 0x22,
                          'end': 0x23,
                          'home': 0x24,
                          'left_arrow': 0x25,
                          'up_arrow': 0x26,
                          'right_arrow': 0x27,
                          'down_arrow': 0x28,
                          'select': 0x29,
                          'print': 0x2A,
                          'execute': 0x2B,
                          'print_screen': 0x2C,
                          'ins': 0x2D,
                          'del': 0x2E,
                          'help': 0x2F,
                          '0': 0x30,
                          '1': 0x31,
                          '2': 0x32,
                          '3': 0x33,
                          '4': 0x34,
                          '5': 0x35,
                          '6': 0x36,
                          '7': 0x37,
                          '8': 0x38,
                          '9': 0x39,
                          'a': 0x41,
                          'b': 0x42,
                          'c': 0x43,
                          'd': 0x44,
                          'e': 0x45,
                          'f': 0x46,
                          'g': 0x47,
                          'h': 0x48,
                          'i': 0x49,
                          'j': 0x4A,
                          'k': 0x4B,
                          'l': 0x4C,
                          'm': 0x4D,
                          'n': 0x4E,
                          'o': 0x4F,
                          'p': 0x50,
                          'q': 0x51,
                          'r': 0x52,
                          's': 0x53,
                          't': 0x54,
                          'u': 0x55,
                          'v': 0x56,
                          'w': 0x57,
                          'x': 0x58,
                          'y': 0x59,
                          'z': 0x5A,
                          'numpad_0': 0x60,
                          'numpad_1': 0x61,
                          'numpad_2': 0x62,
                          'numpad_3': 0x63,
                          'numpad_4': 0x64,
                          'numpad_5': 0x65,
                          'numpad_6': 0x66,
                          'numpad_7': 0x67,
                          'numpad_8': 0x68,
                          'numpad_9': 0x69,
                          'multiply_key': 0x6A,
                          'add_key': 0x6B,
                          'separator_key': 0x6C,
                          'subtract_key': 0x6D,
                          'decimal_key': 0x6E,
                          'divide_key': 0x6F,
                          'F1': 0x70,
                          'F2': 0x71,
                          'F3': 0x72,
                          'F4': 0x73,
                          'F5': 0x74,
                          'F6': 0x75,
                          'F7': 0x76,
                          'F8': 0x77,
                          'F9': 0x78,
                          'F10': 0x79,
                          'F11': 0x7A,
                          'F12': 0x7B,
                          'F13': 0x7C,
                          'F14': 0x7D,
                          'F15': 0x7E,
                          'F16': 0x7F,
                          'F17': 0x80,
                          'F18': 0x81,
                          'F19': 0x82,
                          'F20': 0x83,
                          'F21': 0x84,
                          'F22': 0x85,
                          'F23': 0x86,
                          'F24': 0x87,
                          'num_lock': 0x90,
                          'scroll_lock': 0x91,
                          'left_shift': 0xA0,
                          'right_shift ': 0xA1,
                          'left_control': 0xA2,
                          'right_control': 0xA3,
                          'left_menu': 0xA4,
                          'right_menu': 0xA5,
                          'browser_back': 0xA6,
                          'browser_forward': 0xA7,
                          'browser_refresh': 0xA8,
                          'browser_stop': 0xA9,
                          'browser_search': 0xAA,
                          'browser_favorites': 0xAB,
                          'browser_start_and_home': 0xAC,
                          'volume_mute': 0xAD,
                          'volume_Down': 0xAE,
                          'volume_up': 0xAF,
                          'next_track': 0xB0,
                          'previous_track': 0xB1,
                          'stop_media': 0xB2,
                          'play/pause_media': 0xB3,
                          'start_mail': 0xB4,
                          'select_media': 0xB5,
                          'start_application_1': 0xB6,
                          'start_application_2': 0xB7,
                          'attn_key': 0xF6,
                          'crsel_key': 0xF7,
                          'exsel_key': 0xF8,
                          'play_key': 0xFA,
                          'zoom_key': 0xFB,
                          'clear_key': 0xFE,
                          '+': 0xBB,
                          ',': 0xBC,
                          '-': 0xBD,
                          '.': 0xBE,
                          '/': 0xBF,
                          '`': 0xC0,
                          ';': 0xBA,
                          '[': 0xDB,
                          '\\': 0xDC,
                          ']': 0xDD,
                          "'": 0xDE,
                          '`': 0xC0}
               win32api.keybd_event(VK_CODE['p'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['e'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['n'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['n'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['y'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['spacebar'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['r'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['o'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['u'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['l'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['e'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['t'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['t'], 0, 0, 0)
               time.sleep(.05)
               win32api.keybd_event(VK_CODE['e'], 0, 0, 0)
               time.sleep(2)
               self.mousePos(dataMouse2[4][1])
               tme = self.vremja_str()
               time.sleep(20)
               screen3 = self.ScreenShotChisla('coord_snapshot_vhoda.txt')
               name_screen3_log3 = 'screen3_log3_4' + tme + '.bmp'
               screen3.SaveFile(name_screen3_log3, wx.BITMAP_TYPE_BMP)
               vhod10 = wx.Image('vhod__3__.bmp', type=wx.BITMAP_TYPE_ANY)

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
           self.onPlacewindow("penny roulette - william hill casino")
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
       chicloVrach = random.randint(196, 205)
       while ( steps < chicloVrach):
           screen_control_2 = self.ScreenShotChisla('coord_snapshot_control.txt')
           p_cntr_2 = screen_control_2.GetData()
           chicloVrach = random.randint(196, 205)
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
                           #time.sleep(0.05)
                           file_obj.write(str(i) + '\n')
                           time.sleep(0.05)
                           # chislo = False
                           prod_cikla = False

                           screen_control_2 = self.ScreenShotChisla('coord_snapshot_control.txt')
                           p_cntr_2 = screen_control_2.GetData()
                           break

               print('steps_vnutri_vtorogo_cikla',steps_vnutri_vtorogo_cikla )
               if steps_vnutri_vtorogo_cikla == 40:
                   try:
                       print('steps_vnutri_vtorogo_cikla_doljen byt_click', steps_vnutri_vtorogo_cikla)
                       self.onPlacewindow("penny roulette - william hill casino")
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
                   self.mousePos(dataMouse[6][1]) # закрыть окно рулетки
                   time.sleep(1)
                   self.mousePos(dataMouse2[4][1]) # запустить игру заново
                   time.sleep(20)
                   screen3 = self.ScreenShotChisla('coord_snapshot_vhoda.txt')
                   name_screen3_log3 = 'screen_okna_kudato_log3' + tme + '.bmp'
                   screen3.SaveFile(name_screen3_log3, wx.BITMAP_TYPE_BMP)
                   vhod10 = wx.Image('vhod__3__.bmp', type=wx.BITMAP_TYPE_ANY)
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
                     self.onPlacewindow("penny roulette - william hill casino")
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

                   time.sleep(5)
                   file_obj3 = open('log.txt', 'a')
                   file_obj3.write('cik igry: '+str(self.schet_gig_cikl)+'Beskonechyi vtoroy cikl ' + tme + '\n')
                   file_obj3.close()
                   file_obj.write('avariynoe zavershenie raboty'  + '\n')
                   file_obj.close()
                   game.terminate()
                   time.sleep(180)
                   self.Glavnaja()
                   break
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
       time.sleep(290)
       if self.schet_gig_cikl <26:
           self.Glavnaja()
   def OnButton(self, event):
        """Called when self.btn1 is clicked"""
        self.Glavnaja()
if __name__ == "__main__":
 app = MyApp(False)
 app.MainLoop()