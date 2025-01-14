from abc import ABC, abstractmethod
from typing import Dict, Iterator, Type, List

class MCBotBaseModel(ABC):
    @staticmethod
    @abstractmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        pass

    @staticmethod
    def is_cache_model():
        return True

    @staticmethod
    def filter_optional_params(model_kwargs):
        optional_params = {}
        for key, value in model_kwargs.items():
            if key not in ['model_id', 'use_local', 'streaming']:
                optional_params[key] = value
        return optional_params