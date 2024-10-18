# a simple tuning script
from process_output import process
from visualize import show_run
from wrf_controller import run_WRF




PATH = "/home/capstoneii/Build_WRF/WRF/run"

def tune(var, opts):
    default = params[var]
    failed = []
    for i in opts:
        params[var] = i

        #with open('/home/capstoneii/WRF_Input/namelist-bnl.input', 'r') as reader:
        with open('tuner.input', 'r') as reader:
            with open(f'{PATH}/namelist.input', 'w') as writer:
                writer.write(reader.read().format(**params))  
                
        if run_WRF(PATH, 7, run_real=False):
            show_run(process(PATH, "tuner"), f"{var}_{i}", True, True)
        else:
            failed.append(i)
    params[var] = default
    return failed


params= {
    'vdis': .3,
    'beta_con': 1.0E24,
}

failed = []
#failed.append(tune('shcu_physics', [i for i in range(6)]))

failed.append(tune('vdis', [.15,.3,.6]))

failed.append(tune('beta_con', [1E23,1E24]))
if len(failed):
    print(f'failed at {failed}')
else:
    print("SUCCESS")
