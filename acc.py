import numpy as np

class Accelerometer:
    def __init__(self, dt, alpha=0.2, bias=None, noiseStd=0.1):
        self.dt = dt
        self.alpha = alpha
        
        if bias is not None:
            self.bias = np.array(bias)
        else:
            self.bias = np.array([0.02, -0.01, 0.03])
            
        self.noiseStd = noiseStd
        self.filteredValue = np.array([0.0, 0.0, 0.0])

    def measure(self, trueAcc):
        noise = np.random.normal(0, self.noiseStd, 3)
        rawAcc = np.array(trueAcc) + self.bias + noise
        self.filteredValue = (self.alpha * rawAcc) + ((1 - self.alpha) * self.filteredValue)
        return self.filteredValue
