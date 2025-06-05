# input_providers/base.py

from abc import ABC, abstractmethod

class InputProvider(ABC):
    @abstractmethod
    def get_next_chunk(self):
        """
        Return the next available text chunk.
        For manual input, this could be the full text blob.
        For live input, this could be the next line(s) from the log.
        """
        pass
