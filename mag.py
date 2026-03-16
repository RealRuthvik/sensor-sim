import numpy as np

class Magnetometer:
    def __init__(self, dt, alpha=0.2, bias=None, noiseStd=2.0):
        self.dt = dt
        self.alpha = alpha
        
        if bias is not None:
            self.bias = np.array(bias)
        else:
            self.bias = np.array([1.5, -0.8, 0.5])
            
        self.noiseStd = noiseStd
        self.filteredValue = np.array([0.0, 0.0, 0.0])

    def measure(self, trueB):
        noise = np.random.normal(0, self.noiseStd, 3)
        rawB = np.array(trueB) + self.bias + noise
        self.filteredValue = (self.alpha * rawB) + ((1 - self.alpha) * self.filteredValue)
        return self.filteredValue
