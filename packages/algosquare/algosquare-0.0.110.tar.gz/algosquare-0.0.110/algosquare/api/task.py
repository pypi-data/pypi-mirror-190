"""AlgoSquare Task API."""
from __future__ import annotations

from .api import ApiObject, api_get, api_post, api_delete
from .model import Model
from .algo import Algo

class Task(ApiObject):
    """Task class."""
    @classmethod
    def get(cls, task_id: str) -> Task:
        """
        Gets specific task.
        
        Args:
            task_id: string.

        Returns:
            Task.
        """
        return cls(api_get(f'tasks/{task_id}/api'))

    def refresh(self) -> None:
        """reloads task."""
        self.update(api_get(f'tasks/{self.task_id}/api'))

    def build_models(self, run_time: int = 60, max_algos: int = 10, server_cost: float = 0.2, max_algo_fee: float = 5, algo_ids: list[str] = []) -> None:
        """
        Builds model for task.
        
        Args:
            run_time: time in minutes.
            max_algos: maximum number of algos to use.
            server_cost: maximum server cost per hour in USD.
            max_algo_fee: maximum hourly rate of deployment.
            algo_ids: explicitly provide algos to use.

        Raises:
            RuntimeError, ValueError.
        """
        if self.status != 'inactive':
            raise RuntimeError('status must be inactive')

        run_time = int(run_time)
        if run_time < 5:
            raise ValueError('run_time must be minimum 5')

        payload = dict(run_time = run_time)

        if algo_ids:
            if len(algo_ids) > 20:
                raise ValueError('max 20 algos allowed')

            payload['algo_ids'] = algo_ids
        else:
            max_algos = int(max_algos)
            if max_algos < 1:
                raise ValueError('max_algos must be minimum 1')

            server_cost = float(server_cost)
            if server_cost < 0.2:
                raise ValueError('server_cost must be a minimum of 0.2')

            max_algo_fee = float(max_algo_fee)
            if max_algo_fee < 0:
                raise ValueError('max_algo_fee must not be negative')

            payload['max_algos'] = max_algos
            payload['server_cost'] = server_cost
            payload['max_algo_fee'] = max_algo_fee

        self.update(api_post(f'tasks/{self.task_id}/automl/api', json=payload))

    def stop_build(self) -> None:
        """
        Stops model building.
        
        Raises:
            RuntimeError.
        """
        if self.status != 'building_models':
            raise RuntimeError('status must be building_models')

        self.update(api_delete(f'tasks/{self.task_id}/automl/api'))

    def get_models(self) -> list[Model]:
        """
        Gets models for task.
        
        Returns:
            List of Models.
        """
        return [Model.load(x) for x in api_get(f'models/group/{self.task_id}/api')]

    def get_own_algos(self) -> list[Algo]:
        """
        Gets own algos for task.
        
        Returns:
            List of Algos.
        """
        return [Algo(x) for x in api_get(f'tasks/{self.task_id}/algos/api')]


