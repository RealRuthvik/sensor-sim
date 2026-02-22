import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

timeList = []
axList = []
ayList = []
azList = []

fig, ax = plt.subplots()

lineAX, = ax.plot([], [], label="Accel X")
lineAY, = ax.plot([], [], label="Accel Y")
lineAZ, = ax.plot([], [], label="Accel Z (Gravity)")

ax.set_xlim(0, 10)
ax.set_ylim(-50, 50)
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Acceleration")
ax.legend()

startTime = time.time()
previousTime = startTime

mouseX = 0
mouseY = 0
previousMouseX = 0
previousMouseY = 0

previousVX = 0
previousVY = 0

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
    global previousVX, previousVY

    currentTime = time.time()
    dt = currentTime - previousTime

    if dt == 0:
        dt = 0.001

    previousTime = currentTime

    # Position change
    dx = mouseX - previousMouseX
    dy = mouseY - previousMouseY

    previousMouseX = mouseX
    previousMouseY = mouseY

    # Velocity
    vx = dx / dt * 0.01
    vy = dy / dt * 0.01

    # Acceleration (derivative of velocity)
    ax_val = (vx - previousVX) / dt
    ay_val = (vy - previousVY) / dt
    az_val = 9.8  # simulate gravity

    previousVX = vx
    previousVY = vy

    elapsedTime = currentTime - startTime

    timeList.append(elapsedTime)
    axList.append(ax_val)
    ayList.append(ay_val)
    azList.append(az_val)

    if elapsedTime > 10:
        ax.set_xlim(elapsedTime - 10, elapsedTime)

    lineAX.set_data(timeList, axList)
    lineAY.set_data(timeList, ayList)
    lineAZ.set_data(timeList, azList)

    return lineAX, lineAY, lineAZ


ani = FuncAnimation(fig, update, interval = 50)
plt.show()