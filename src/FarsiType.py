from pynput import keyboard
from plyer.utils import platform
from plyer import notification
import subprocess
import ctypes
import pyautogui
import time
import os
import sys

class AdobeConnectFarsiType:
    def __init__(self):

        if(self.ProcessExists('connect.exe') == False):
            print('Your Adobe Connect is not running!')
            notification.notify(
                title='Adobe Connect Farsi Type',
                message='Your Adobe Connect is not running!',
                app_name='Adobe Connect Farsi Type',
            )
            sys.exit(0)

        if(self.KeyBoardLayout_Hex() == '0x429'):
            print('To use, please make your keyboard language English first!\nThen the program automatically changes your keyboard to Persian.')
            notification.notify(
                title='Adobe Connect Farsi Type',
                message='To use, please make your keyboard language English first!\nThen the program automatically changes your keyboard to Persian.',
                app_name='Adobe Connect Farsi Type',
            )
            sys.exit(0)
        
        pyautogui.hotkey('alt', 'shift') # Change Language To Farsi
        self.COMBINATIONS = []
        for com in self.Farsi_Combinations():
            self.COMBINATIONS.append({keyboard.KeyCode(char=com)})
        self.current = set()
        print('Adobe Connect Farsi Type Enabled !')
        notification.notify(
                title='Adobe Connect Farsi Type',
                message='Adobe Connect Farsi Type Enabled !',
                app_name='Adobe Connect Farsi Type',
        )
        with keyboard.Listener(on_press=self.OnAnyKeyPressed, on_release=self.OnAnyKeyReleased) as listener:
            listener.join()

    def KeyBoardLayout_Hex(self):
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        cwin = user32.GetForegroundWindow()
        klid = user32.GetKeyboardLayout(user32.GetWindowThreadProcessId(cwin, 0))
        language_id = klid & (2**16 - 1)
        return hex(language_id)
    
    def Farsi_Combinations(self):
        return {
            'd':b'\xd9\x8a',
            'ی':b'\xd9\x8a',
        }

    def ProcessExists(self, Process):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % Process
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(Process.lower())

    def Farsi_Formatter(self, key):
        if(str(self.KeyBoardLayout_Hex()) == '0x429'):
            key = self.Farsi_Combinations()[str(key).replace("'", '')]
            key_name = key.decode()
            time.sleep(0.015)
            pyautogui.press('backspace')
            os.system('echo '+key_name+'|clip')
            pyautogui.hotkey('ctrl', 'v')

    def OnAnyKeyPressed(self, key):
        if any([key in COMBO for COMBO in self.COMBINATIONS]):
            self.current.add(key)
            if any(all(k in self.current for k in COMBO) for COMBO in self.COMBINATIONS):
                self.Farsi_Formatter(key)

    def OnAnyKeyReleased(self, key):
        if any([key in COMBO for COMBO in self.COMBINATIONS]):
            self.current.remove(key)

app = AdobeConnectFarsiType()