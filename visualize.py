import matplotlib.pyplot as plt
import numpy as np

def show_run(run, name, GT = False, scatter = False):
    from extract_GT import get_GT
    plt.clf()
    if GT:
        gt = get_GT()
        plt.plot(run[:,0], gt, label = "GT")
        plt.title("DOWN MSE: {:.2} TOT MSE: {:.2}".format(np.mean((gt - run[:,1])**2), np.mean((gt - run[:,4])**2)))
    if scatter:
        plt.scatter(run[:,0], run[:,1], label = "SWDOWN")
        plt.scatter(run[:,0], run[:,4], label = "DIR + DIF")
    else:
        plt.scatter(run[:,0], run[:,1], label = "SWDOWN")
        plt.scatter(run[:,0], run[:,4], label = "DIR + DIF")
    plt.legend()
    plt.savefig('output_images/' + name + '.jpg')
def show_bnl(runs, name):
    plt.clf()
    for domain, run in enumerate(runs):
        plt.plot(run[0], run[-1], label=f'TOT_{domain}')
    plt.legend()
    plt.savefig('output_images/' + name + '.jpg')