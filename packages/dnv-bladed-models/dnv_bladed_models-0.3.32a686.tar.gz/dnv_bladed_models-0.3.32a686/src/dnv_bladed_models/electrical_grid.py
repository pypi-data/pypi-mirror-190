# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401
from enum import Enum, IntEnum

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Type, Union, Callable  # noqa: F401
from pathlib import Path
from typing import TypeVar
Model = TypeVar('Model', bound='BaseModel')
StrBytes = Union[str, bytes]

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, root_validator, Extra  # noqa: F401

from dnv_bladed_models.dnv import Dnv

from dnv_bladed_models.grid_loss_energy_sink import GridLossEnergySink


class ElectricalGrid(Dnv):
    """ElectricalGrid - The definition of the electrical grid that the turbine is connected to.

    Attributes:
        - NetworkVoltage: float => A number representing an electrical voltage [https://ww.wikipedia.org/wiki/Voltage].  The SI units for volatage are Volts.
        - ConnectingLineResistance: float => A number representing an electrical resistance [https://www.wikipedia.org/wiki/Electrical_resistance_and_conductance].  The SI units for resistance are Ohms, ℧.
        - ConnectingLineInductance: float => A number representing an electrical inductance [https://www.wikipedia.org/wiki/Inductance].  The SI units for inductance are henrys (H).
        - NetworkResistance: float => A number representing an electrical resistance [https://www.wikipedia.org/wiki/Electrical_resistance_and_conductance].  The SI units for resistance are Ohms, ℧.
        - NetworkInductance: float => A number representing an electrical inductance [https://www.wikipedia.org/wiki/Inductance].  The SI units for inductance are henrys (H).
        - NumberOfTurbinesOnFarm: int => The number of turbines on the farm that share the same grid connection.
        - GridLossEnergySinks: List[GridLossEnergySink] => A list of energy sinks available to the turbine.
    """

    NetworkVoltage: Optional[float] = Field(alias="NetworkVoltage", default=None)
    ConnectingLineResistance: Optional[float] = Field(alias="ConnectingLineResistance", default=None)
    ConnectingLineInductance: Optional[float] = Field(alias="ConnectingLineInductance", default=None)
    NetworkResistance: Optional[float] = Field(alias="NetworkResistance", default=None)
    NetworkInductance: Optional[float] = Field(alias="NetworkInductance", default=None)
    NumberOfTurbinesOnFarm: Optional[int] = Field(alias="NumberOfTurbinesOnFarm", default=None)
    GridLossEnergySinks: Optional[List[GridLossEnergySink]] = Field(alias="GridLossEnergySinks", default=list())

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass

    @root_validator(pre=True)
    def parsing_ignores_underscore_properties(cls, values: dict[str, any]):
        allowed_vals = {}
        for key, val in values.items():
            if not key.startswith('_'):
                if isinstance(val, dict):
                    allowed_child_vals = {}
                    for child_key, child_val in val.items():
                        if not child_key.startswith('_'):
                            allowed_child_vals[child_key] = child_val
                    allowed_vals[key] = allowed_child_vals
                else:
                    allowed_vals[key] = val
        return allowed_vals

    def to_json(
        self,
        *, 
        include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None, 
        exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None, 
        by_alias: bool = True, 
        skip_defaults: Optional[bool] = None, 
        exclude_unset: bool = False, 
        exclude_defaults: bool = False, 
        exclude_none: bool = True, 
        encoder: Optional[Callable[[Any], Any]] = None, 
        models_as_dict: bool = True, 
        **dumps_kwargs: Any) -> str:

        r"""
        Generates a JSON string representation of the model.
        
        Notes
        -----
        `include` and `exclude` arguments as per `dict()`.

        `encoder` is an optional function to supply as `default` to json.dumps(), other arguments as per `json.dumps()`.

        Examples
        --------
        >>> model.to_json()

        Renders the full JSON representation of the model object.
        """

        if dumps_kwargs.get('indent') is None:
            dumps_kwargs.update(indent=2)

        return super().json(
                include=include, 
                exclude=exclude, 
                by_alias=by_alias, 
                skip_defaults=skip_defaults, 
                exclude_unset=exclude_unset, 
                exclude_defaults=exclude_defaults, 
                exclude_none=exclude_none, 
                encoder=encoder, 
                models_as_dict=models_as_dict, 
                **dumps_kwargs)
    
    @classmethod
    def from_file(
        cls: Type['Model'],
        path: Union[str, Path]) -> 'Model':
        
        r"""
        Loads a model from a given file path.

        Parameters
        ----------
        path : string
            The file path to the model.

        Returns
        -------
        ElectricalGrid
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ElectricalGrid.from_file('/path/to/file')
        """
        
        return super().parse_file(path=path)
    
    @classmethod
    def from_json(
        cls: Type['Model'],
        b: StrBytes) -> 'Model':

        r"""
        Creates a model object from a JSON string.

        Parameters
        ----------
        b: StrBytes
            The JSON string describing the model.

        Returns
        -------
        ElectricalGrid
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ElectricalGrid.from_json('{ ... }')
        """

        return super().parse_raw(
            b=b,
            content_type='application/json')
    
    @classmethod
    def from_dict(
        cls: Type['Model'],
         obj: Any) -> 'Model':

        r"""
        Creates a model object from a dict.

        Parameters
        ----------
        obj : Any
            The dictionary object describing the model.

        Returns
        -------
        ElectricalGrid
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.
        """
        
        return super().parse_obj(obj=obj)
    
    def to_file(
        self,
        path: Union[str, Path]):

        r"""
        Writes the model as a JSON document to a file with UTF8 encoding.        

        Parameters
        ----------                
        path : string
            The file path to which the model will be written.

        Examples
        --------
        >>> model.to_file('/path/to/file')

        """

        with open(file=path, mode='w', encoding="utf8") as output_file:
            output_file.write(self.to_json())

ElectricalGrid.update_forward_refs()
