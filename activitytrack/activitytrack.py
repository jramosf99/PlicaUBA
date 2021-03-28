from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import pandas as pd
import time
from datetime import datetime
import os

outputPath = "/home/ramos/Escritorio/TFG/activitytrack/data/data.csv" #path of the CSV output file

class Counter:
    pulsations = 0
    clicks = 0
    moves = 0
    scrolls = 0
    def reset(self):
        self.pulsations = 0
        self.clicks = 0
        self.moves = 0
        self.scrolls = 0
counter = Counter

def on_press(key):
    counter.pulsations += 1


def on_move(x, y):
    counter.moves += 1

def on_click(x, y, button, pressed):
    if pressed:
        counter.clicks += 1


def on_scroll(x, y, dx, dy):
    counter.scrolls += 1


# Setup the listener threads
keyboard_listener = KeyboardListener(on_press=on_press, on_release=None)
mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

# Start the threads and join them so the script doesn't end early
keyboard_listener.start()
mouse_listener.start()


while True:
    minute = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(2)
    df=pd.DataFrame([[minute,counter.clicks,counter.pulsations, counter.moves, counter.scrolls]], columns=["date","clicks","pulsations","moves","scrolls"],index=None)
    if not os.path.isfile(outputPath):
        df.to_csv(outputPath, index=None, header=True)
    else:
        df.to_csv(outputPath, index=None, mode='a', header=False)
    Counter.reset(counter)
