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


class EvolvingWindTurbulence_MethodEnum(str, Enum):
    KRISTENSEN = "KRISTENSEN"
    EXPONENTIAL = "EXPONENTIAL"

class EvolvingWindTurbulence_ApplyToEnum(str, Enum):
    OFF = "OFF"
    LIDAR_ONLY = "LIDAR_ONLY"
    ALL_WIND_CALCULATIONS = "ALL_WIND_CALCULATIONS"

class EvolvingWindTurbulence(Dnv):
    """EvolvingWindTurbulence - The settings for evolving turbulence.  In the case of a normal turbulent wind field, the turbulence is frozen and approaches the turbine at a constant block.  Although this doesn&#39;t match physical reality, it is a particular problem for Lidar - as it gives them a perfect insight into the oncoming wind field.  In order to represent the nature of real turbulence, a second turbulence file is superimposed on the windfield so that it evolves as it moves forward.  This is computationally expensive, and is usually applied only to the Lidar readings - although it can be applied to all the wind values in a simulation.

    Attributes:
        - SecondTurbulenceFilepath: str => The filepath or URI of the second turbulence file.  The turbulence in this file will be used to simulate an evolving turbulence field.
        - Method: EvolvingWindTurbulence_MethodEnum => The method used to combine the turbulence in the two turbulence files.
        - ExponentialFactor: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - ApplyTo: EvolvingWindTurbulence_ApplyToEnum => Evolving turbulence is usually only applied to Lidar readings, but it can be applied to all wind values.
    """

    SecondTurbulenceFilepath: Optional[str] = Field(alias="SecondTurbulenceFilepath", default=None)
    Method: Optional[EvolvingWindTurbulence_MethodEnum] = Field(alias="Method", default=None)
    ExponentialFactor: Optional[float] = Field(alias="ExponentialFactor", default=None)
    ApplyTo: Optional[EvolvingWindTurbulence_ApplyToEnum] = Field(alias="ApplyTo", default=None)

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
        EvolvingWindTurbulence
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = EvolvingWindTurbulence.from_file('/path/to/file')
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
        EvolvingWindTurbulence
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = EvolvingWindTurbulence.from_json('{ ... }')
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
        EvolvingWindTurbulence
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

EvolvingWindTurbulence.update_forward_refs()
