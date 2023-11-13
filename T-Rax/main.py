import datetime

import pyautogui as m
import numpy as np

size = m.size()

x = 0.3700 * size[0]  #3650
y = 0.3620 * size[1] #низкие 3820  только высокие: 3450

width = 120

constant = np.array(m.screenshot(region=(x, y, width, 2)))

m .moveTo( x, y)
now = datetime.datetime.now()
while True:
    tree = m.screenshot(region=(x,  y,  width, 2))
    ar = np.array(tree)


    if not np.array_equal(ar, constant):
        m.press( 'space')

    if now.second % 10  == 0 and width != 180:
        width += 8  
    constant = ar
