import wx


# Some classes to use for the notebook pages.  Obviously you would
# want to use something more meaningful for your application, these
# are just for illustration.

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Кнопка определения иконки игры", (20,20))
        btn = wx.Button(self, label="Press Me")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 5)
        sizer.Add(t, 0, wx.ALL, 5)
        self.SetSizer(sizer)

class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent) # создаем панель
        staticbox0 = wx.StaticBox(self, wx.NewId(), label="StaticBox") # создаем ГЛАВНЫЙ раздел на весь сайзер
        sizer_00 = wx.StaticBoxSizer(staticbox0, wx.VERTICAL) # Создаем сайзер который будет размещать элементы на панели
                                                          # и кладываем в него ГЛАВНЫЙ раздел
        staticbox01 = wx.StaticBox(self, wx.NewId(), label="StaticBox 1") # создаем внутрен раздел 01
        staticbox02 = wx.StaticBox(self, wx.NewId(), label="StaticBox 2") # создаем внутрен раздел 02

        sizer_01 = wx.StaticBoxSizer(staticbox01, wx.VERTICAL) # создаем вложенные сайзер_01
        sizer_02 = wx.StaticBoxSizer(staticbox02, wx.VERTICAL) # создаем вложенные сайзер_02
        sizer_00.Add(sizer_01) # и добавляем сайзер_01 в 00_siser
        sizer_00.Add(sizer_02) # и добавляем сайзер_02 в 00_siser
                               # алтернатива размещения "(sizer_02, flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)"
       # создаем различные элементы окна
        t = wx.StaticText(self, -1, "This is a PageTwo object", (40, 40))

        btn1 = wx.Button(self, wx.NewId(), "Button 1")
        btn2 = wx.Button(self, wx.NewId(), "Button 2")
        btn3 = wx.Button(self, wx.NewId(), "Button 3")
        btn4 = wx.Button(self, wx.NewId(), "Button 4")
        # привязываем элементы окна к разделам
        sizer_01.Add(t)
        sizer_01.Add(btn1)
        sizer_01.Add(btn2)

        sizer_02.Add(btn3)
        sizer_02.Add(btn4)

        self.SetSizer(sizer_00) # привязываем все к главному сайзеру

        self.Layout()

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a PageThree object", (60,60))


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Simple Notebook Example")

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page1 = PageOne(nb)
        page2 = PageTwo(nb)
        page3 = PageThree(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Page 1")
        nb.AddPage(page2, "Page 2")
        nb.AddPage(page3, "Page 3")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()