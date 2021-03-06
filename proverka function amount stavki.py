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

    def ScreenShotChisla(self, coordinaty):
        """
        Делает скриншот выбранного фрагмента экрана
        Основано на методе, предложенном Андреа Гавана
        """

        with open(coordinaty, 'r') as f:  # извлекаем  из файла
            data2 = json.load(f)
        # print('', data2)
        rect1 = data2
        # print('rect', rect1)

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
    def proverkaStavki(self,dataPic_razmer_stavok):
           print('проверка велечины ставки')
           time.sleep(0.2)
           screen_stavki = self.ScreenShotChisla('coord_snapshot_amount_stavki.txt')
           p1 = screen_stavki.GetData()
           screen_stavki.SaveFile('proverka_stavok.bmp', wx.BITMAP_TYPE_BMP)
           resulte = 99
           for i in range(len(dataPic_razmer_stavok)):
               # print('razmer spiska stavok ', len(dataPic_razmer_stavok))
               # print('cikl nomer', i)
               # prod_cikla = True
               # p = screen.GetData()
               time.sleep(0.01)
               p2 = dataPic_razmer_stavok[i].GetData()
               nome = 'proverka_stavok'+str(i)+'.bmp'
               dataPic_razmer_stavok[i].SaveFile(nome , wx.BITMAP_TYPE_BMP)
               # print("зашли в цикл")
               time.sleep(0.01)
               if p1 == p2:
                   print("razmer stavki_funk", i)
                   resulte = i
           return resulte
    def initial_pic_stavok(self):
          pic=[]
          for i in range(3):
               name = 'stavka'+str(i)+'.bmp'
               name = wx.Image(name, type=wx.BITMAP_TYPE_ANY)
               pic.append(name)
          return   pic
    def Glavnaja(self):
        dataPic_razmer_stavok = self.initial_pic_stavok()
        razmer = self.proverkaStavki(dataPic_razmer_stavok)
        print('razmer stavki', razmer)
    def OnButton(self, event):
        """Called when self.btn1 is clicked"""
        self.Glavnaja()
if __name__ == "__main__":
 app = MyApp(False)
 app.MainLoop()