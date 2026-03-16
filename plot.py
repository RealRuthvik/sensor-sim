import numpy as np
import matplotlib.pyplot as plt
from acc import Accelerometer
from gyro import Gyroscope
from mag import Magnetometer

# This class and methods within this class were made with help from ai.

class RotationalDynamics:
    def __init__(self, inertia):
        self.inertia = np.array(inertia)
        self.invInertia = np.linalg.inv(self.inertia)
        self.omega = np.array([0.5, 0.1, -0.2])
        self.q = np.array([1.0, 0.0, 0.0, 0.0])

    def propagate(self, dt, torque=np.array([0.0, 0.0, 0.0])):
        omegaX = np.array([
            [0, -self.omega[0], -self.omega[1], -self.omega[2]],
            [self.omega[0], 0, self.omega[2], -self.omega[1]],
            [self.omega[1], -self.omega[2], 0, self.omega[0]],
            [self.omega[2], self.omega[1], -self.omega[0], 0]
        ])
        dq = 0.5 * omegaX @ self.q
        self.q = self.q + dq * dt
        self.q = self.q / np.linalg.norm(self.q)

        alpha = self.invInertia @ (torque - np.cross(self.omega, self.inertia @ self.omega))
        self.omega = self.omega + alpha * dt
        return self.omega

    def getBodyMagneticField(self, bInertial):
        q0, q1, q2, q3 = self.q
        R = np.array([
            [1 - 2*(q2**2 + q3**2), 2*(q1*q2 + q0*q3), 2*(q1*q3 - q0*q2)],
            [2*(q1*q2 - q0*q3), 1 - 2*(q1**2 + q3**2), 2*(q2*q3 + q0*q1)],
            [2*(q1*q3 + q0*q2), 2*(q2*q3 - q0*q1), 1 - 2*(q1**2 + q2**2)]
        ])
        return R @ bInertial

class SensorSuite:
    def __init__(self, dt, alpha=0.2):
        self.acc = Accelerometer(dt, alpha)
        self.gyro = Gyroscope(dt, alpha)
        self.mag = Magnetometer(dt, alpha)

    def getMeasurements(self, trueAcc, trueOmega, trueB):
        accMeas = self.acc.measure(trueAcc)
        omega_estimated = self.gyro.measure(trueOmega)
        B_measured = self.mag.measure(trueB)
        return accMeas, omega_estimated, B_measured

dt = 0.05
timeSteps = 400
timeArr = np.linspace(0, timeSteps * dt, timeSteps)

inertiaMatrix = np.diag([0.010, 0.015, 0.012])
dynamics = RotationalDynamics(inertiaMatrix)

suiteHeavy = SensorSuite(dt, 0.05)
suiteLight = SensorSuite(dt, 0.3)

trueAccList = []
trueOmegaList = []
trueBList = []

measAccHeavy = []
measOmegaHeavy = []
measBHeavy = []

measAccLight = []
measOmegaLight = []
measBLight = []

bInertial = np.array([20.0, -10.0, 30.0])
sensorOffset = np.array([0.05, 0.0, 0.0])

i = 0
while i < timeSteps:
    omegaTrue = dynamics.propagate(dt)
    bTrue = dynamics.getBodyMagneticField(bInertial)
    
    accTrue = np.cross(omegaTrue, np.cross(omegaTrue, sensorOffset))
    
    trueAccList.append(accTrue)
    trueOmegaList.append(omegaTrue)
    trueBList.append(bTrue)
    
    aH, oH, bH = suiteHeavy.getMeasurements(accTrue, omegaTrue, bTrue)
    measAccHeavy.append(aH)
    measOmegaHeavy.append(oH)
    measBHeavy.append(bH)
    
    aL, oL, bL = suiteLight.getMeasurements(accTrue, omegaTrue, bTrue)
    measAccLight.append(aL)
    measOmegaLight.append(oL)
    measBLight.append(bL)
    
    i = i + 1

trueAccList = np.array(trueAccList)
trueOmegaList = np.array(trueOmegaList)
trueBList = np.array(trueBList)

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
    axs[j, 0].plot(timeArr, trueAccList[:, j], label="True", color='black', linewidth=2)
    axs[j, 0].plot(timeArr, measAccLight[:, j], label="Light Filter", alpha=0.7)
    axs[j, 0].plot(timeArr, measAccHeavy[:, j], label="Heavy Filter", alpha=0.7)
    axs[j, 0].set_ylabel("Acc " + axisLabels[j])
    axs[j, 0].grid(True)
    
    axs[j, 1].plot(timeArr, trueOmegaList[:, j], label="True", color='black', linewidth=2)
    axs[j, 1].plot(timeArr, measOmegaLight[:, j], label="Light Filter", alpha=0.7)
    axs[j, 1].plot(timeArr, measOmegaHeavy[:, j], label="Heavy Filter", alpha=0.7)
    axs[j, 1].set_ylabel("Gyro " + axisLabels[j])
    axs[j, 1].grid(True)
    
    axs[j, 2].plot(timeArr, trueBList[:, j], label="True", color='black', linewidth=2)
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
