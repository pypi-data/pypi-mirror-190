from typing import Dict, List

from dstack.backend.aws.config import AWSConfig
from dstack.core.config import BackendConfig


def list_config() -> List[BackendConfig]:
    configs = [cls() for cls in BackendConfig.__subclasses__()]  # pylint: disable=E1101
    return configs


def list_dict() -> Dict[str, BackendConfig]:
    configs = [cls() for cls in BackendConfig.__subclasses__()]  # pylint: disable=E1101
    names = {}
    for config in configs:
        if config.configured:
            names[config.name] = config

    return names
