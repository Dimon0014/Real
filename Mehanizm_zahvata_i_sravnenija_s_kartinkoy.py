# snapshot и сравнивает с картинкой из файла
import json
import sys
import wx
from time import clock
import win32ui, win32gui, win32con, win32api


class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Screenshot Tutorial")

        panel = wx.Panel(self)
        screenshotBtn = wx.Button(panel, label="Take Screenshot")
        screenshotBtn.Bind(wx.EVT_BUTTON, self.onTakeScreenShot)
       # printBtn = wx.Button(panel, label="Print Screenshot")
        #printBtn.Bind(wx.EVT_BUTTON, self.onPrint)
        panel.SetBackgroundColour(wx.WHITE)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(screenshotBtn, 0, wx.ALL | wx.CENTER, 5)
        #sizer.Add(printBtn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

    def pix_to_pix(x, y, im1, im2):
        for i in range(0, x, 4):
            for k in range(0, y, 4):
                f_ = (i, k)
                p = im1.GetRed(f_)
                p2 = im2.GetRed(f_)
                if p == p2:
                    print('x=', i, 'y=', k)
                    if f_ == (x - 4, y - 4):
                        print('у картинок пикселы равны')
                else:
                    print('пикселы не равны')
                    break
    def onTakeScreenShot(self, event):
        """
        Делает скриншот выбранного фрагмента экрана
        Основано на методе, предложенном Андреа Гавана
        """
        start1 = clock()
        with open('coord_snapshot_vhoda.txt', 'r') as f:  # извлекаем  из файла
            data2 = json.load(f)
        print('', data2)
        rect1 = data2  # win32gui.GetWindowRect(hwnd)
       # mfcDC = win32ui.CreateDCFromHandle(hwnd)
        print('rect', rect1)

        rect = self.GetRect() #  получаем координаты своего окна
        rect.x = rect1[0]#+134
        rect.y = rect1[1]#+275
        rect.width = rect1[2]-rect1[0]#+1080)
        rect.height = rect1[3]- rect1[1]#+691)
        #print('координаты', rect.x, rect.y, rect.width, rect.height)
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
        memDC.SelectObject(wx.NullBitmap) # освобождаем память от битмапа, прежде чем снова ее задействовать
                                          # освобождение будет автоматическим если больше не буде обращения к
                                          #  объекту  wx.MemoryDC. То есть освобождать надо если планируем еще
                                          #  использовать для другой картинки. В данном случае можно и не освобождать
        name='vhod2.bmp'
        #
        bmp0 =wx.Image(name, type=wx.BITMAP_TYPE_ANY)
        name = 'vhod_2.bmp'
        #
        bmp1 = wx.Image(name, type=wx.BITMAP_TYPE_ANY)
        # bmp2 =wx.Bitmap(bmp0)
        # name3 = 'myImage2.bmp'
        # bmp3 = wx.Image(name3, type=wx.BITMAP_TYPE_ANY, index=-1)
        # bmp4 = wx.Bitmap(bmp3)
        pixel=bmp1.GetRed(0,0)
        print('pixel',pixel)
        img = bmp.ConvertToImage() # конвертация в изображение которое можно вывести на экран
        # img0 = bmp0.ConvertToImage()
        # img1 = bmp1.ConvertToImage()
        # img2 = bmp2.ConvertToImage()
        # img3 = bmp4.ConvertToImage()
        p = img.GetData()
        p2 = bmp1.GetData()
        # h1 = hash(p)
        # h2 = hash(p2)
        if p == p2:
             print("равны")
        else:
             print("не равны")
        # fileName = "myImage_2_.bmp"
        # fileName2 = "myImage_02_.bmp"
        # fileName3 = "myImage_02_3.bmp"


        img.SaveFile('vhod__2.bmp', wx.BITMAP_TYPE_BMP)
        # img2.SaveFile(fileName2, wx.BITMAP_TYPE_BMP)
        # img3.SaveFile(fileName3, wx.BITMAP_TYPE_BMP)
        # f_=(0, 0)
        # p = img0.getpixel(f_)
        # p2 = img1.getpixel(f_)
        if bmp0 == bmp1:
            print(' равны')
        #self.pix_to_pix(78, 57, bmp0, bmp1)
        # for i in range(0, 78, 4):
        #     for k in range(0, 57, 4):
        #         f_ = [76, 56]
        #         p = bmp0.GetRed(i,k)
        #         p2 = bmp1.GetRed(i,k)
        #         if p == p2:
        #             print('x=', i, 'y=', k)
        #             if f_ == [i , k ]:
        #                 print('у картинок пикселы равны')
        #         else:
        #             print('пикселы не равны')
        #             break


        print('...saving as BMP!')

        end1 = clock()

        print("Result (iterativ): выполняется за " + "\nФункция %1.10f секунд" % (end1 - start1))


# Запустите программу
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()