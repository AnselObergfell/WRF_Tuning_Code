import matplotlib.pyplot as plt
import numpy as np
from extract_GT import get_GT
start = 8
end = -1
LCB = np.load("Bayesian_Opt_LCB/func_vals.npy")
PI = np.load("Bayesian_Opt_PI/func_vals.npy")
EI = np.load("Bayesian_Opt_EI/func_vals.npy")
base = np.load("cached_runs/WRF0.5022518796518519-8.842030068192521e+21.npy").T[:,-1]
gt = get_GT()
MSE = np.mean((gt - base)**2)
plt.plot(LCB[start:end], marker = 'o', label = "LCB")
plt.plot(EI[start:end], marker = 'x',label = "EI")
plt.plot(PI[start:end], marker = '*', label = "PI")
plt.axhline(MSE, color = 'r', linestyle = '--', label="base")
plt.plot()
plt.title("")
plt.ylabel("Error")
plt.xlabel("Number of Itterations")
plt.legend()
plt.savefig("fig.png")