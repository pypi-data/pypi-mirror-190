import logging
from numbers import Number
from typing import Generic, TypeVar, Union

import numpy as np

from argos.utils.cls import checkType, isAnArray, checkIsAnArray, arrayIsStructured

logger = logging.getLogger(__name__)

Data = TypeVar('Data', bound=np.ndarray)
#FillValue = TypeVar('FillValue', bool, np.bool_, Number, str)

FillValue = TypeVar('FillValue', bound=Union[bool, np.bool_, Number, str])

class ArrayWithMask(Generic[Data, FillValue]):
    def __init__(self, data: Data, fill_value: FillValue):
        self._data: Data = data
        self.data = data

        self._fill_value: FillValue = fill_value
        self.fill_value= fill_value


    @property
    def data(self) -> Data:
        """ The array values. Will be a numpy array."""
        return self._data


    @data.setter
    def data(self, values: Data) -> None:
        """ The array values. Must be a numpy array."""
        #checkIsAnArray(values)
        self._data = values


    @property
    def fill_value(self) -> FillValue:
        """ The fill_value."""
        return self._fill_value


    @fill_value.setter
    def fill_value(self, fill_value: FillValue):
        """ The fill_value."""
        self._fill_value = fill_value
