import win32com.client

xlApp = win32com.client.Dispatch("Excel.Application")
filename,password = r"encryptedtest.xlsx", '123456'
xlwb = xlApp.Workbooks.Open(filename, False, True, None, Password=password)
print(dir(xlApp.Workbooks))
print(xlwb.Sheets(1).Cells(1,1))