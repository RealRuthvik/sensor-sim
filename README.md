# Sensor Sim
A Python based simulation of rigid body rotational dynamics and sensor measurements. It models an Accelerometer, Gyroscope, and Magnetometer with adjustable noise, bias, and first order low pass filtering.

# Features
* Rotational Dynamics: Quaternion based propagation of a rigid body's orientation and angular velocity.
* Sensor Models: Simulates raw sensor readings by injecting Gaussian noise and static bias into true values.
* Signal Processing: Implements an exponential moving average filter to smooth noisy measurements.
* Visualization: Plots true dynamics against lightly and heavily filtered sensor data across all three axes.
