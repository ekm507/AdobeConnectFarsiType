from pynput import keyboard
from plyer import notification
import subprocess
import ctypes
import pyautogui
import time
import os
import sys

class AdobeConnectFarsiType:
    def __init__(self):

        self.on_verify = False

        if(self.ProcessExists('connect.exe') == False):
            print('Your Adobe Connect is not running!')
            notification.notify(
                title='Adobe Connect Farsi Type',
                message='Your Adobe Connect is not running!',
                app_name='Adobe Connect Farsi Type',
            )
            sys.exit(0)

        self.COMBINATIONS = []
        for com in self.Farsi_Combinations():
            self.COMBINATIONS.append({keyboard.KeyCode(char=com)})
        self.current = set()
        
        with keyboard.Listener(on_press=self.OnAnyKeyPressed, on_release=self.OnAnyKeyReleased) as listener:
            time.sleep(1)
            pyautogui.press('a')
            listener.join()
    
    def Farsi_Combinations(self):
        return {
            'd':b'\xd9\x8a',
            'ی':b'\xd9\x8a'
        }

    def NotifyStart(self):
        pyautogui.hotkey('alt', 'shift') # Change Language To Farsi
        print('Adobe Connect Farsi Type Enabled !')
        notification.notify(
                title='Adobe Connect Farsi Type',
                message='Adobe Connect Farsi Type Enabled !',
                app_name='Adobe Connect Farsi Type',
        )

    def NotifyLanguageError(self):
        print('To use, please make your keyboard language English first!\nThen the program automatically changes your keyboard to Persian.')
        notification.notify(
            title='Adobe Connect Farsi Type',
            message='To use, please make your keyboard language English first!\nThen the program automatically changes your keyboard to Persian.',
            app_name='Adobe Connect Farsi Type',
        )
        sys.exit(0)

    def ProcessExists(self, Process):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % Process
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(Process.lower())

    def Farsi_Formatter(self, key):
        time.sleep(0.015)
        pyautogui.press('backspace')
        pyautogui.hotkey('shift', 'x')

    def OnAnyKeyPressed(self, key):
        if(self.on_verify == False):
            if key == keyboard.KeyCode(char='a'):
                if(self.on_verify == False):
                    self.on_verify = True
                    pyautogui.press('backspace')
                    self.NotifyStart() # Start App
            else:
                self.on_verify = True
                self.NotifyLanguageError() # Byebye


        if any([key in COMBO for COMBO in self.COMBINATIONS]):
            self.current.add(key)
            if any(all(k in self.current for k in COMBO) for COMBO in self.COMBINATIONS):
                self.Farsi_Formatter(key)

    def OnAnyKeyReleased(self, key):
        if any([key in COMBO for COMBO in self.COMBINATIONS]):
            self.current.remove(key)

app = AdobeConnectFarsiType()