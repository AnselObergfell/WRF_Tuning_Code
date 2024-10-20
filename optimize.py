import numpy as np
import wrf_controller as Controller
import extract_GT
from skopt import gp_minimize as BO
from skopt.utils import use_named_args
from skopt.space import Real, Integer, Categorical
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import os


dim_vdis     = Real(low=.01, high=1.40, name='vdis')
dim_beta_con = Real(low=1e+20, high=1e+24, name='beta_con', prior='log-uniform')
dimensions  = [dim_vdis, dim_beta_con]

def save_strat(res, folder):
    if folder not in os.listdir():
        os.mkdir(folder)
    np.save(os.path.join(folder, "func_vals.npy"), res['func_vals'])
    #plt.plot(sorted(res['func_vals'], reverse=True)[4:])
    plt.plot(res['func_vals'])
    vdis, beta_con = res['x']
    print(res['x'], res['fun'])
    plt.title("found {:.3f} at vdis={:.3f}, beta_con={:.2E}".format(res['fun'], vdis, beta_con))
    plt.xlabel('epoch')
    plt.ylabel('MSE')
    plt.savefig(os.path.join(folder,'optimization_path.png'))
    return 1

@use_named_args(dimensions=dimensions)
def evaluate(**params):
    pred = Controller.run_model(params).T[:,-1]
    gt   = extract_GT.get_GT()
    print("\n--- EVALUATING CURRENT RESULTS ---")  
    MSE = np.mean((gt - pred)**2)
    print(params)
    print(f"--- MSE: {MSE} ---\n")
    return MSE

def Bayesian_Opt(iterations=10, seed=123):
    result = BO(func=evaluate, dimensions=dimensions, n_calls=np.int32(iterations), noise=0.1, random_state=np.int32(seed), acq_func="PI")
    print("BEST PARAMS:", result['x'])
    print("EVAL:", result['fun'])
    if "Bayesian_Opt" not in os.listdir():
        os.mkdir("Bayesian_Opt")
    return result


def kiefer_wolfowitz1d(iterations = 10, seed = 123):
    vdis = .3
    beta_con = 1.0e24
    func_vals = []
    initial_result = evaluate([vdis, beta_con])
    func_vals.append(initial_result)
    best_fun = initial_result
    best_x = [vdis, beta_con]
    
    for n in range(1,iterations+1):
        cn = n**(-1/3)*.3/2
        N1 = evaluate([np.clip(vdis + cn, 0.01, 1.4) ,beta_con])
        N2 = evaluate([np.clip(vdis - cn, 0.01, 1.4) ,beta_con])
        func_vals.append((N1 + N2) / 2)
        if best_fun > func_vals[-1]:
            func_vals.append(best_fun)
            best_x = [vdis, beta_con]
        vdis = np.clip(vdis + 1/n * (N1 - N2) / (2*cn), .01, 1.4)

    if "Kiefer_Wolfowitz1D" not in os.listdir():
        os.mkdir("Kiefer_Wolfowitz1D")
    return {'func_vals': np.array(func_vals), 'fun': best_fun, 'x': best_x}


def optimize(strategy, iterations = 10, seed=5):
    strategies = ['BO', 'KW', 'KW1D']
    if strategy == 'BO':
        return Bayesian_Opt(iterations, seed)
    #if strategy == 'KW':
        #return kiefer_wolfowitz(iterations, seed)
    if strategy == 'KW1D':
        return kiefer_wolfowitz1d(iterations, seed)
    print(f"Currently supported strategies are:\n{', '.join(strategies)}")
    

if __name__ == "__main__":
    #save_strat(optimize('KW1D', 8), "Kiefer_Wolfowitz1D")
    #save_strat(optimize('KW', 10), "Kiefer_Wolfowitz")
    save_strat(optimize('BO', 15), "Bayesian_Opt")