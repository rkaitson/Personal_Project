from ray import tune

from ax_config import AxOptimizer
from PID_t import Simulation
import PID_config as config
import pandas as pd


def evalfn(params):

    kp = params['Kp']
    ki = params['Ki']
    kd = params['Kd']

    sim = Simulation(kp, ki, kd)    
    metrics = sim.cycle()
 

    if metrics == -1: exit()

    metrics['Kp'] = kp
    metrics['Ki'] = ki
    metrics['Kd'] = kd
    
    print(metrics)

    #m_df = pd.DataFrame.from_dict(metrics,orient='columns')
    #m_df.to_pickle(f"Users/rkaitson/PID/Jar/run_{kp}_{ki}_{kd}.pkl")
    
    tune.report(val_score=metrics['SAIE'])


if __name__ == '__main__':

    #config = {'Kp': 0.1, 'Ki': 0.01, 'Kd': 0.5}
    #evalfn(config)
    print('Loaded modules')
    ## run optimization
    config = {'settings':config.settings,
              'params':config.params}
    hyperopt = AxOptimizer(config)
    print('Starting run')
    hyperopt.run(evalfn)
