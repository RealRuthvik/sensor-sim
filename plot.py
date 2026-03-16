import numpy as np
import matplotlib.pyplot as plt
from acc import Accelerometer
from gyro import Gyroscope
from mag import Magnetometer

class SensorSuite:
    def __init__(self, dt, alpha=0.2):
        self.acc = Accelerometer(dt, alpha)
        self.gyro = Gyroscope(dt, alpha)
        self.mag = Magnetometer(dt, alpha)

    def getMeasurements(self, trueAcc, trueOmega, trueB):
        accMeas = self.acc.measure(trueAcc)
        omegaMeas = self.gyro.measure(trueOmega)
        bMeas = self.mag.measure(trueB)
        return accMeas, omegaMeas, bMeas

dt = 0.1
timeSteps = 200
timeArr = np.linspace(0, 20, timeSteps)

trueAcc = np.array([np.sin(timeArr * 0.3), np.cos(timeArr * 0.3), np.ones(timeSteps) * 9.8]).T
trueOmega = np.array([np.sin(timeArr * 0.5), np.cos(timeArr * 0.5), np.sin(timeArr * 0.2)]).T
trueB = np.array([np.cos(timeArr * 0.1) * 30, np.sin(timeArr * 0.1) * 30, np.ones(timeSteps) * 10]).T

suiteHeavy = SensorSuite(dt, 0.1)
suiteLight = SensorSuite(dt, 0.5)

measAccHeavy = []
measOmegaHeavy = []
measBHeavy = []

measAccLight = []
measOmegaLight = []
measBLight = []

i = 0
while i < timeSteps:
    aH, oH, bH = suiteHeavy.getMeasurements(trueAcc[i], trueOmega[i], trueB[i])
    measAccHeavy.append(aH)
    measOmegaHeavy.append(oH)
    measBHeavy.append(bH)
    
    aL, oL, bL = suiteLight.getMeasurements(trueAcc[i], trueOmega[i], trueB[i])
    measAccLight.append(aL)
    measOmegaLight.append(oL)
    measBLight.append(bL)
    
    i = i + 1

measAccHeavy = np.array(measAccHeavy)
measOmegaHeavy = np.array(measOmegaHeavy)
measBHeavy = np.array(measBHeavy)

measAccLight = np.array(measAccLight)
measOmegaLight = np.array(measOmegaLight)
measBLight = np.array(measBLight)

fig, axs = plt.subplots(3, 3, figsize=(15, 10), sharex=True)
axisLabels = ['X', 'Y', 'Z']

j = 0
while j < 3:
    axs[j, 0].plot(timeArr, trueAcc[:, j], label="True", color='black', linewidth=2)
    axs[j, 0].plot(timeArr, measAccLight[:, j], label="Light Filter", alpha=0.7)
    axs[j, 0].plot(timeArr, measAccHeavy[:, j], label="Heavy Filter", alpha=0.7)
    axs[j, 0].set_ylabel("Acc " + axisLabels[j])
    axs[j, 0].grid(True)
    
    axs[j, 1].plot(timeArr, trueOmega[:, j], label="True", color='black', linewidth=2)
    axs[j, 1].plot(timeArr, measOmegaLight[:, j], label="Light Filter", alpha=0.7)
    axs[j, 1].plot(timeArr, measOmegaHeavy[:, j], label="Heavy Filter", alpha=0.7)
    axs[j, 1].set_ylabel("Gyro " + axisLabels[j])
    axs[j, 1].grid(True)
    
    axs[j, 2].plot(timeArr, trueB[:, j], label="True", color='black', linewidth=2)
    axs[j, 2].plot(timeArr, measBLight[:, j], label="Light Filter", alpha=0.7)
    axs[j, 2].plot(timeArr, measBHeavy[:, j], label="Heavy Filter", alpha=0.7)
    axs[j, 2].set_ylabel("Mag " + axisLabels[j])
    axs[j, 2].grid(True)
    
    j = j + 1

axs[2, 0].set_xlabel("Time (s)")
axs[2, 1].set_xlabel("Time (s)")
axs[2, 2].set_xlabel("Time (s)")
axs[0, 2].legend(loc="upper right")

plt.tight_layout()
plt.show()