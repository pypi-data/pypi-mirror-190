import contextlib
import os
import logging
import multiprocessing

logger = logging.getLogger('pystematic.torch')

@contextlib.contextmanager
def envvars(env):
    original_environ = os.environ.copy()
    os.environ.update(env)
    yield
    os.environ.clear()
    os.environ.update(original_environ)

class ProcessQueue:

    def __init__(self, num_processes, gpu_ids=[], num_gpus_per_process=None):
        self._mp_context = multiprocessing.get_context('spawn')
        self._num_processes = num_processes
        self._num_gpus_per_process = num_gpus_per_process
        self._live_processes = []

        self._gpu_resource = Resource(gpu_ids)

    def _wait(self):
        sentinels = [proc.sentinel for proc in self._live_processes]
        finished_sentinels = multiprocessing.connection.wait(sentinels)

        completed_procs = []
        
        for proc in self._live_processes:
            if proc.sentinel in finished_sentinels:
                completed_procs.append(proc)

        for proc in completed_procs:
            if self._num_gpus_per_process is not None:
                self._gpu_resource.free(proc.gpus)
            self._live_processes.remove(proc)

    def run_and_wait_for_completion(self, experiment, list_of_params):

        for params in list_of_params:

            while len(self._live_processes) >= self._num_processes:
                self._wait()
            
            if self._num_gpus_per_process is not None:
                gpus = self._gpu_resource.allocate(self._num_gpus_per_process)

                with envvars({"CUDA_VISIBLE_DEVICES": ",".join([str(id) for id in gpus])}):
                    proc = experiment.run_in_new_process(params)
                    proc.gpus = gpus
                    self._live_processes.append(proc)
            else:
                
                proc = experiment.run_in_new_process(params)
                self._live_processes.append(proc)
            
        while len(self._live_processes) > 0:
            self._wait()


class Resource:
    #TODO: add allocation cap and distinct option

    def __init__(self, resource_ids):
        self._resources = {}

        for id in resource_ids:
            self._resources[id] = 0

    def allocate(self, num_resources):
        if num_resources > len(self._resources):
            raise ValueError(f"There are only '{len(self._resources)}' distinct "
                             f"resources available. Tried to allocate '{num_resources}'.")
        
        ids_with_least_count = sorted(self._resources.keys(), key=lambda id: self._resources[id])[:num_resources]

        for id in ids_with_least_count:
            self._resources[id] += 1

        return ids_with_least_count

    def free(self, resource_ids):
        for id in resource_ids:
            if self._resources[id] <= 0:
                logger.warn(f"Tried to free resource with id '{id}' which is unallocated (count is '{self._resources[id]}').")
            else:
                self._resources[id] -= 1
