import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

timeList = []
bxList = []
byList = []
bzList = []

fig, ax = plt.subplots()

lineBX, = ax.plot([], [], label="Mag X")
lineBY, = ax.plot([], [], label="Mag Y")
lineBZ, = ax.plot([], [], label="Mag Z")

ax.set_xlim(0, 10)
ax.set_ylim(-60, 60)
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Magnetic Field (µT)")
ax.legend()

startTime = time.time()
heading = 0

mouseX = 0
previousMouseX = 0
firstMove = True

# mouse capture refined by AI
def mouseMoved(event):
    global mouseX, previousMouseX, firstMove

    if event.x is not None:
        if firstMove:
            previousMouseX = event.x
            firstMove = False
        mouseX = event.x

fig.canvas.mpl_connect("motion_notify_event", mouseMoved)

def update(frame):
    global heading, previousMouseX

    currentTime = time.time()
    elapsedTime = currentTime - startTime

    dx = mouseX - previousMouseX
    previousMouseX = mouseX
    
    heading += dx * 0.01

    B = 50

    bx = B * np.cos(heading)
    by = B * np.sin(heading)
    bz = 10 

    # noise added by AI
    bx += np.random.normal(0, 1)
    by += np.random.normal(0, 1)
    bz += np.random.normal(0, 0.5)

    timeList.append(elapsedTime)
    bxList.append(bx)
    byList.append(by)
    bzList.append(bz)

    if elapsedTime > 10:
        ax.set_xlim(elapsedTime - 10, elapsedTime)

    lineBX.set_data(timeList, bxList)
    lineBY.set_data(timeList, byList)
    lineBZ.set_data(timeList, bzList)

    return lineBX, lineBY, lineBZ

ani = FuncAnimation(fig, update, interval=50)

plt.show()
