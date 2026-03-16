import numpy as np

class Gyroscope:
    def __init__(self, dt, alpha=0.2, bias=None, noiseStd=0.02):
        self.dt = dt
        self.alpha = alpha
        
        if bias is not None:
            self.bias = np.array(bias)
        else:
            self.bias = np.array([0.005, -0.002, 0.001])
            
        self.noiseStd = noiseStd
        self.filteredValue = np.array([0.0, 0.0, 0.0])

    def measure(self, trueOmega):
        noise = np.random.normal(0, self.noiseStd, 3)
        rawOmega = np.array(trueOmega) + self.bias + noise
        self.filteredValue = (self.alpha * rawOmega) + ((1 - self.alpha) * self.filteredValue)
        return self.filteredValue
