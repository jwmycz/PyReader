from Wxframe.index import *

if __name__ == "__main__":
    try:
        app = wx.App()
        frame = MainFrame(None)
        frame.Show()
        app.MainLoop()
    except Exception as e:
        print("程序异常退出:", e)
        input("按回车退出...")