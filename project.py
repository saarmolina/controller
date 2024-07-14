import wx
from threading import Thread
from PIL import ImageGrab
import time
from time import gmtime, strftime
import socket


def scale_bitmap(bitmap, width, height): # Function to scale bitmap to specified width and height
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result



class Client(wx.Frame):
    def __init__(self, parent, title):
        super(Client, self).__init__(parent, title="Control Panel", size=(1920, 1080)) # Create a frame with specified size and title
        self.clientS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket for communication
        self.SetBackgroundColour((0, 0, 0)) # Set background color to black
        self.SetDoubleBuffered(True)
        self.Centre() # Center the frame
        self.Show() # Show the frame

        self.picture = wx.StaticBitmap(self, pos=(0, 0)) # Create a static bitmap for displaying images
        self.bg = wx.StaticBitmap(self, pos=(0, 170)) # Create a static bitmap for background

        self.bg.SetBitmap(wx.Bitmap('bg.jpg')) # Set the background image

        wx.Button(self, label='CONNECT', pos=(650, 60), id=2) # Create a CONNECT button
        self.Bind(wx.EVT_BUTTON, self.connectServer, id=2) 

        wx.Button(self, label='Play', pos=(750, 60), id=4) # Create a Play button to start video
        self.Bind(wx.EVT_BUTTON, self.showVideo, id=4)

        wx.Button(self, label='Lock', pos=(850, 60), id=6) # Create a Lock button to lock the screen
        self.Bind(wx.EVT_BUTTON, self.lock, id=6)

        wx.Button(self, label='Unlock', pos=(950, 60), id=7) # Create an Unlock button to unlock the screen
        self.Bind(wx.EVT_BUTTON, self.unlock, id=7)

        wx.Button(self, label='Shut Down', pos=(1050, 60), id=8) # Create a Shut Down button
        self.Bind(wx.EVT_BUTTON, self.shutdown, id=8)

        wx.Button(self, label='EXIT', pos=(1150, 60), id=9) # Create an EXIT button
        self.Bind(wx.EVT_BUTTON, self.exitCon, id=9)


        self.picture.Bind(wx.EVT_MOTION, self.showMouse) # Bind the mouse motion event to showMouse method

        self.picture.Bind(wx.EVT_LEFT_DCLICK, self.doubleClick) # Bind the double click event to doubleClick method

        self.picture.Bind(wx.EVT_LEFT_DOWN, self.leftDown) # Bind the left mouse button down event to leftDown method

        self.picture.Bind(wx.EVT_LEFT_UP, self.leftUp) # Bind the left mouse button up event to leftUp method

        self.Bind(wx.EVT_KEY_DOWN, self.press) # Bind the key down event to press method

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.nope)

        self.Bind(wx.EVT_PAINT, self.paint)

        self.isConnected = False # Initialize connection status to False
    
    

    def connectServer(self, e): # Method to connect to the server
        if (self.isConnected == False):
            self.clientS.connect(('192.168.1.51', 33000))
            print "connected"
            self.isConnected = True
            self.SetFocus()



    def showVideo(self, e): # Method to show the video
        self.videoRun = True
        try:
            self.picture.Show()
        except:
            print ""
        self.t1 = Thread(target=self.video)
        self.t1.start()
        self.SetFocus()
        
    def video(self): # Thread method to run the video
        self.bg.Hide()
        while self.videoRun == True:
            self.clientS.send('screenshot')
            sc = self.clientS.recv(7000000)
            time.sleep(0.001)
            self.img = wx.ImageFromData(1920, 1080, sc)
            self.picture.SetBitmap(scale_bitmap(wx.BitmapFromImage(self.img), 1920, 1040))
            self.SetFocus()

    def stopVideo(self, e):
        self.videoRun = False

    def showMouse(self, e): # Method to handle mouse movement on the screen
        if self.isConnected:
            self.t2 = Thread(target=self.mouse, args=(e,))
            self.t2.start()
            self.mouse(e)

    def mouse(self, e): # Thread method to send mouse position to the server
        if self.isConnected:
            self.a = e.GetPositionTuple()
            self.x, self.y = self.a
            self.clientS.send("mouse:" + str(self.x) + ":" + str(self.y) + "?")

    def doubleClick(self, e): # Method to handle double click event
        if self.isConnected:
            self.clientS.send("doubleClick")

    def leftUp(self, e): # Method to handle left mouse button up event
        if self.isConnected:
            self.clientS.send("leftUp")

    def leftDown(self, e): # Method to handle left mouse button down event
        if self.isConnected:
            self.clientS.send("leftDown")

    def press(self, e): # Method to handle key press events
        if self.isConnected:
            if (e.GetKeyCode() == 27):
                self.picture.Hide()
                self.videoRun = False
                self.picture.Hide()
                self.bg.Show()
                
            else:
                self.clientS.send("keyboard:" + str(e.GetKeyCode()) + "?")

    def lock(self, e): # Method to lock the screen
        if self.isConnected:
            self.clientS.send("lock")


    def unlock(self, e): # Method to unlock the screen
        if self.isConnected:
            self.clientS.send("unlock")

    def exitCon(self, e): # Method to exit the connection
        if self.isConnected:
            self.clientS.send('exit')
            self.clientS.close()

    def shutdown(self, e): # Method to shut down the server
        self.clientS.send("shutDown")

    def nope(self, e):
        pass

    def paint(self, e):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(0, 0, self.GetSize()[0], self.GetSize()[1])

          
        

        
        



    #----------------------------------------------------------------------

            
     


if __name__ == '__main__':
 
    app = wx.App()
    Client(None, title='Center')
    app.MainLoop()
