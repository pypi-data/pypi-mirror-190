"""AlgoSquare Package API."""
from __future__ import annotations

import os
import json

from .api import ApiObject, api_get, api_post
from .common import upload_file
from .predictor import Predictor

class Package(ApiObject):
    """Package class."""
    @classmethod
    def upload(cls, file: str) -> Package:
        """
        Creates a new package.
        
        Args:
            file: .whl file.

        Returns:
            Package.
        """
        if not file.endswith('.whl'):
            raise ValueError('file must be a .whl file')

        if not os.path.isfile(file):
            raise FileNotFoundError('file does not exist')

        files = [dict(namespace = "package", filename = os.path.split(file)[-1], key = upload_file(file))]    
        return cls(api_post('packages/api', json=dict(files = files)))

    @classmethod
    def get(cls, package_id: str) -> Package:
        """
        Gets specific package.
        
        Args:
            package_id: string.

        Returns:
            Package.
        """
        return cls(api_get(f'packages/{package_id}/api'))

    def refresh(self) -> None:
        """reloads task."""
        self.update(api_get(f'packages/{self.package_id}/api'))

    def get_predictors(self) -> list[Predictor]:
        """
        Gets predictors for package.
        
        Returns:
            List of Predictors.
        """
        if self.status != 'ok':
            raise RuntimeError('status must be ok')

        return [Predictor(x) for x in api_get(f'predictors/package/{self.package_id}/api')]