import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

timeList = []
xList = []
yList = []
zList = []

fig, ax = plt.subplots()

lineX, = ax.plot([], [], label="Mouse X")
lineY, = ax.plot([], [], label="Mouse Y")
lineZ, = ax.plot([], [], label="Mouse Z (N/A)")

ax.set_xlim(0, 10)
ax.set_ylim(-10, 10)
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Angular Velocity")
ax.legend()

startTime = time.time()
previousTime = startTime

mouseX = 0
mouseY = 0
previousMouseX = 0
previousMouseY = 0
firstMove = True


def mouseMoved(event):
    global mouseX, mouseY, previousMouseX, previousMouseY, firstMove

    if event.x is not None and event.y is not None:
        if firstMove:
            previousMouseX = event.x
            previousMouseY = event.y
            firstMove = False

        mouseX = event.x
        mouseY = event.y


fig.canvas.mpl_connect("motion_notify_event", mouseMoved)


def update(frame):
    global previousTime, previousMouseX, previousMouseY

    currentTime = time.time()
    dt = currentTime - previousTime

    if dt == 0:
        dt = 0.001

    previousTime = currentTime

    dx = mouseX - previousMouseX
    dy = mouseY - previousMouseY

    previousMouseX = mouseX
    previousMouseY = mouseY

    xRate = dx / dt * 0.005
    yRate = dy / dt * 0.005
    zRate = 0

    elapsedTime = currentTime - startTime

    timeList.append(elapsedTime)
    xList.append(xRate)
    yList.append(yRate)
    zList.append(zRate)

    if elapsedTime > 10:
        ax.set_xlim(elapsedTime - 10, elapsedTime)

    lineX.set_data(timeList, xList)
    lineY.set_data(timeList, yList)
    lineZ.set_data(timeList, zList)

    return lineX, lineY, lineZ


ani = FuncAnimation(fig, update, interval = 50)
plt.show()