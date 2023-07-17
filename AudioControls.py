from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import time
import pyautogui
import os
from pyvda import VirtualDesktop

class AudioControlsClass:
    def prediction_gesture_handler(self,predictions):
        #print(predictions)
        count =0
        past_gestures = predictions[-15:]
        for i in range(len(past_gestures)):
            #print(past_gestures[-i])
            if past_gestures[-1] == past_gestures[-i]:
                count = count + 1
        if count > 10:
            return past_gestures[-1]
        else:
            return "gesture 7"
        
    def change_volume(self,volume_delta):
        # Get the default audio device
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        # Get the current volume level
        volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = volume_control.GetMasterVolumeLevelScalar()

        # Calculate the new volume level
        new_volume = max(0.0, min(1.0, current_volume + volume_delta))

        # Set the new volume level
        volume_control.SetMasterVolumeLevelScalar(new_volume, None)

    def increase_volume(self):
        self.change_volume(0.05)  # Increase the volume by 0.1 (or any desired increment)

    def decrease_volume(self):
        self.change_volume(-0.05)  # Decrease the volume by 0.1 (or any desired decrement)

    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')


    def trigger_file_explorer(self):
        folder_path = "C:/Users/rohit"
        os.system(f'start "" "{folder_path}"')

    def switch_to_next_tab(self):
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.keyUp('alt')
        pyautogui.keyUp('enter')

    def playpause(self):
        pyautogui.press('playpause')


    def switch_to_previous_desktop(self):
        VirtualDesktop(2).go()


