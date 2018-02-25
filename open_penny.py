import pywinauto
from pywinauto.application import Application


app = Application().start('C:\Program Files (x86)\William Hill Casino\casino.exe')

# describe the window inside Notepad.exe process
dlg_spec = app.UntitledNotepad
# wait till the window is really open
actionable_dlg = dlg_spec.wait('visible')

print(actionable_dlg)