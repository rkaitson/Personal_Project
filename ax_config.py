import torch
import os
import ray
from ray import tune
import logging
from ray.tune.suggest.ax import AxSearch
from ax.service.ax_client import AxClient

class AxOptimizer(object):
    def __init__(self, config):
        ray.init(log_to_driver=False)
        logger = logging.getLogger(tune.__name__)
        logger.setLevel(level=logging.CRITICAL)
        # https://github.com/ray-project/ray/issues/28328
        os.environ["PL_DISABLE_FORK"] = "1"
        # settings for bayesian optimization
        self.settings = config['settings']
        self.device = torch.device('cpu')
        # hyperparameters
        self.params = config['params']
        # create ax experiment for raytune search
        self.ax = AxClient(enforce_sequential_optimization=False)
        self.exp = self.ax.create_experiment(
            name=self.settings['name'],
            parameters=self.params,
            objective_name=self.settings['metric'],
            minimize=self.settings['minimize'],
        )
        self.search_alg = AxSearch(ax_client=self.ax)

    def run(self, axopt_evaluation_function):

        # execute raytune hyperparameter search
        tune.run(
            axopt_evaluation_function,
            name=self.settings['name'],
            num_samples=self.settings['num_samples'],
            search_alg=self.search_alg,
            resources_per_trial={
                # 'gpu': 1,
                'cpu': 10
            },
            verbose=1,
            raise_on_failed_trial=False,
            checkpoint_freq=0,
        )

        # save information from search algorithm
        self.ax.save_to_json_file(filepath=self.settings['name']+'.json')
