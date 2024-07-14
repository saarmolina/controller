import wx
from threading import Thread
from PIL import ImageGrab
import time
from time import gmtime, strftime
import socket


def scale_bitmap(bitmap, width, height): #����� ����� ���� �� �����
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result



class Client(wx.Frame):
    def __init__(self, parent, title):
        super(Client, self).__init__(parent, title="Control Panel",size=(1920, 1080)) #����� �� ���� ���� ������� ���
        self.clientS=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #����� ����� �� ���� 
        self.SetBackgroundColour((0,0,0)) #����� �� ��� ����
        self.SetDoubleBuffered(True)
        self.Centre() #�� �� ����� �����
        self.Show() #���� �� �����

        self.picture = wx.StaticBitmap(self, pos=(0,0)) #������� �� ������ ����� �� ������ ���� 
        self.bg = wx.StaticBitmap(self, pos=(0,170)) #������� �� ������ ����� �� ����

        self.bg.SetBitmap(wx.Bitmap('bg.jpg')) #���� �� ����

        wx.Button(self, label='CONNECT', pos=(650, 60),id=2) #����� ������ ������
        self.Bind(wx.EVT_BUTTON, self.connectServer,id = 2) 

        wx.Button(self, label='Play', pos=(750, 60),id=4) #����� ������ ����� ��� ����� ����
        self.Bind(wx.EVT_BUTTON, self.showVideo,id = 4)

        wx.Button(self, label='Lock', pos=(850, 60),id=6) #����� ������ �� ����� ����� ����
        self.Bind(wx.EVT_BUTTON, self.lock,id = 6)

        wx.Button(self, label='Unlock', pos=(950, 60),id=7) #����� ������ �� ����� ������ �� ����� ���� 
        self.Bind(wx.EVT_BUTTON, self.unlock,id = 7)

        wx.Button(self, label='Shut Down', pos=(1050, 60),id=8) #����� ������ �� ����� ����� ����
        self.Bind(wx.EVT_BUTTON, self.shutdown,id = 8)

        wx.Button(self, label='EXIT', pos=(1150, 60),id=9) #����� ������ �� ����� ������ 
        self.Bind(wx.EVT_BUTTON, self.exitCon,id = 9)


        self.picture.Bind(wx.EVT_MOTION, self.showMouse) #����� �� ����� �� �����

        self.picture.Bind(wx.EVT_LEFT_DCLICK, self.doubleClick) #����� �� ����� ����� ���� ������ �� ����� 

        self.picture.Bind(wx.EVT_LEFT_DOWN, self.leftDown) #����� �� ��� ���� ������ �� ����� ����

        self.picture.Bind(wx.EVT_LEFT_UP, self.leftUp) #����� �� ��� ���� ������ �� ����� �� ����

        self.Bind(wx.EVT_KEY_DOWN, self.press) #����� �� ����� �� ��� ������

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.nope)

        self.Bind(wx.EVT_PAINT, self.paint)

        self.isConnected=False #����� ����� ����� �� ���� ����� ����
    
    

    def connectServer (self, e): #����� ������� ������ �� ����
        if (self.isConnected==False):
            self.clientS.connect(('192.168.1.51', 33000))
            print "connected"
            self.isConnected=True
            self.SetFocus()



    def showVideo (self, e): #����� ������ �� ������ ����
        self.videoRun=True
        try:
            self.picture.Show()
        except:
            print ""
        self.t1 = Thread(target = self.video)
        self.t1.start()
        self.SetFocus()
        
    def video(self): #Thread ����� �� ������ ���� ����� ����
        self.bg.Hide()
        while self.videoRun==True:
            self.clientS.send('screenshot')
            sc=self.clientS.recv(7000000)
            time.sleep(0.001)
            self.img=wx.ImageFromData(1920, 1080, sc)
            self.picture.SetBitmap(scale_bitmap(wx.BitmapFromImage(self.img),1920,1040))
            self.SetFocus()

    def stopVideo (self, e):
        self.videoRun=False

    def showMouse (self, e): #����� ������� �� ���� �� ����� �� �����
        if self.isConnected:
            self.t2 = Thread(target = self.mouse, args=(e,))
            self.t2.start()
            self.mouse(e)

    def mouse (self, e): #Thread ����� ���� �� ������ ����� ����� ����
        if self.isConnected:
            self.a=e.GetPositionTuple()
            self.x, self.y= self.a
            self.clientS.send("mouse:"+str(self.x)+":"+str(self.y)+"?")

    def doubleClick (self, e): #����� ������� �� ���� �� ����� �����
        if self.isConnected:
            self.clientS.send("doubleClick")

    def leftUp (self, e): #����� ������� �� ���� ������� ����
        if self.isConnected:
            self.clientS.send("leftUp")

    def leftDown (self, e): #����� ������� �� ���� ������� ������
        if self.isConnected:
            self.clientS.send("leftDown")

    def press (self, e): #����� ������� �� ����� ������ ������ ������ 
        if self.isConnected:
            if (e.GetKeyCode()==27):
                self.picture.Hide()
                self.videoRun=False
                self.picture.Hide()
                self.bg.Show()
                
            else:
                self.clientS.send("keyboard:"+str(e.GetKeyCode())+"?")

    def lock (self, e): #����� ������� �� ���� �� ������ ��� 
        if self.isConnected:
            self.clientS.send("lock")


    def unlock (self, e): #����� ������� �� ���� �� ������ ��� 
        if self.isConnected:
            self.clientS.send("unlock")

    def exitCon (self,e): #���� �� ������
        if self.isConnected:
            self.clientS.send('exit')
            self.clientS.close()

    def shutdown (self,e): #����� ������� �� ���� �� ������
        self.clientS.send("shutDown")

    def nope (self, e):
        pass

    def paint (self, e):
        dc=wx.PaintDC(self)
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0,0,self.GetSize()[0],self.GetSize()[1])

          
        

        
        



    #----------------------------------------------------------------------
    

            
     


if __name__ == '__main__':
 
	app = wx.App()
	Client(None, title='Center')
	app.MainLoop()




