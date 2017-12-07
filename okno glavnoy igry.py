import wx, sys
import json
import win32api, win32gui, win32con, time
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
       i = 0
       for item in data2:  # приводим к типу Python
           self.data_fin2.append(list(item))

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

   def initial_pic(self):
      pic=[]
      for i in range(38):
           name = str(i)+'.bmp'
           name = wx.Image(name, type=wx.BITMAP_TYPE_ANY)
           pic.append(name)
      return   pic
   def OnButton(self, event):
        """Called when self.btn1 is clicked"""
        start1 = clock()

        file_obj = open('real_01.txt', 'a')
        dataMouse = self.initial_x_y()
        dataPic =  self.initial_pic()
        #print[dataPic]
        self.mousePos(dataMouse[0][1])
        time.sleep(0.2)
        # self.leftClick()
        time.sleep(6)
        self.mousePos(dataMouse[1][1])
        time.sleep(7)
        self.onPlacewindow("европейская рулетка премиум - william hill casino")
        time.sleep(7)
        self.mousePos(dataMouse[2][1])
        steps = 0
        seconds = 0
        while (steps<2):
            start = clock()
            first0 = time.time()
            steps=steps+1
            file_obj.write('n xoda'+str(steps) + '\n')
            steps_vnutri_pervogo_cikla = 0
            while (True):
                time.sleep(2)
                steps_vnutri_pervogo_cikla = steps_vnutri_pervogo_cikla +1
                screen = self.ScreenShotChisla('coord_snapshot.txt')
                p = screen.GetData()
                p2 = dataPic[37].GetData()
                if p == p2:
                    #print("есть вращение")
                    #prod_cikla = False
                    break
                else:
                   # time.sleep(0.1)
                    self.mousePos(dataMouse[2][1])
            steps_vnutri_vtorogo_cikla = 0
            while (True):
                time.sleep(0.3)
                steps_vnutri_vtorogo_cikla = steps_vnutri_vtorogo_cikla + 1
                screen = self.ScreenShotChisla('coord_snapshot.txt')
                p = screen.GetData()
                p2 = dataPic[37].GetData()
                if p == p2:
                    #print("вращение не закончилось")
                    # prod_cikla = False
                    continue
                else:
                    #chislo=True
                    for i in range(len(dataPic)):
                        prod_cikla = True
                        #p = screen.GetData()
                        #time.sleep(0.05)
                        p2 = dataPic[i].GetData()
                        if p == p2:
                            print("выпал номер", i)


                            file_obj.write(str(i) + '\n')


                            # chislo = False
                            prod_cikla = False

                            break

               # print('steps_vnutri_vtorogo_cikla',steps_vnutri_vtorogo_cikla )
                if  not prod_cikla:
                   break
            end1 = clock()
            print('steps',steps,'Время:',end1-start)
            first1 = time.time()
            seconds = seconds+(first1-first0)
            if seconds> 16:
                seconds=0
                screen = self.ScreenShotChisla('coord_snapshot_prodolj.txt')
                p = screen.GetData()
                prodolji = wx.Image('prodoljenie.bmp', type=wx.BITMAP_TYPE_ANY)
                p2 = prodolji.GetData()
                if p == p2:
                    self.mousePos(dataMouse[45][1])
        end1 = clock()
        promejutok =end1-start1
        file_obj.write('время работы' + str(promejutok) + '\n')
        file_obj.close()
        time.sleep(0.6)
        self.mousePos(dataMouse[6][1])
        time.sleep(1)
        self.mousePos(dataMouse[7][1])
        time.sleep(1)
        self.mousePos(dataMouse[46][1])
if __name__ == "__main__":
 app = MyApp(False)
 app.MainLoop()