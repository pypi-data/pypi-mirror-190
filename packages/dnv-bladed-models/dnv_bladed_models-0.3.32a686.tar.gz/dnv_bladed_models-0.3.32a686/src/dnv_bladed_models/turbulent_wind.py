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

from dnv_bladed_models.evolving_wind_turbulence import EvolvingWindTurbulence

from dnv_bladed_models.time_domain_wind import TimeDomainWind


class TurbulentWind_CentreTurbulenceFileOnEnum(str, Enum):
    CENTRED_ON_HUB = "CENTRED_ON_HUB"
    BEST_FIT = "BEST_FIT"
    USER_SPECIFIED = "USER_SPECIFIED"

class TurbulentWind_InterpolationMethodEnum(str, Enum):
    LINEAR = "LINEAR"
    CUBIC_IN_ROTOR_PLANE = "CUBIC_IN_ROTOR_PLANE"
    ALL_CUBIC = "ALL_CUBIC"

class TurbulentWind(TimeDomainWind, WindType='TurbulentWind'):
    """TurbulentWind - The definition of a turbulent flow field, with the values for the turbulence defined in an external file.

    Attributes:
        - MeanSpeed: float => A number representing a velocity.  The SI units for velocity are metres per second.
        - TurbulenceFilepath: str => The filepath or URI of the turbulence file. 
        - TurbulenceIntensity: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - TurbulenceIntensityLateral: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - TurbulenceIntensityVertical: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - CentreTurbulenceFileOn: TurbulentWind_CentreTurbulenceFileOnEnum => The method used to position the data in the turbulence file relative to the turbine.  If any part of the rotor exceeds this box, the simulation will terminate with an exception.
        - InterpolationMethod: TurbulentWind_InterpolationMethodEnum => The method used to interpolate the wind speed inbetween the provided turbulence locations.
        - RepeatTurbulenceFile: bool => If true, the turbulence file will be \&quot;looped\&quot;.  If false, the turbulence will be 0 in all three components once the end of the file has been reached.  Using part of a turbulence file may invalidate its turbulence statistics, and no effort is made by Bladed to ensure coherence at the point when it transitions from the end of the wind file back to the beginning.
        - EvolvingTurbulence: EvolvingWindTurbulence 
        - TurbulenceFileStartTime: float => A number representing a time.  The SI units for time are seconds.
        - WindType: str [Read-only] => Allows the schema to identify the type of the object.  For this type of object, this must always be set to &#39;TurbulentWind&#39;
    """

    MeanSpeed: Optional[float] = Field(alias="MeanSpeed", default=None)
    TurbulenceFilepath: Optional[str] = Field(alias="TurbulenceFilepath", default=None)
    TurbulenceIntensity: Optional[float] = Field(alias="TurbulenceIntensity", default=None)
    TurbulenceIntensityLateral: Optional[float] = Field(alias="TurbulenceIntensityLateral", default=None)
    TurbulenceIntensityVertical: Optional[float] = Field(alias="TurbulenceIntensityVertical", default=None)
    CentreTurbulenceFileOn: Optional[TurbulentWind_CentreTurbulenceFileOnEnum] = Field(alias="CentreTurbulenceFileOn", default=None)
    InterpolationMethod: Optional[TurbulentWind_InterpolationMethodEnum] = Field(alias="InterpolationMethod", default=None)
    RepeatTurbulenceFile: Optional[bool] = Field(alias="RepeatTurbulenceFile", default=None)
    EvolvingTurbulence: Optional[EvolvingWindTurbulence] = Field(alias="EvolvingTurbulence", default=None)
    TurbulenceFileStartTime: Optional[float] = Field(alias="TurbulenceFileStartTime", default=None)
    WindType: Optional[str] = Field(alias="WindType", default='TurbulentWind', allow_mutation=False)

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
        TurbulentWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TurbulentWind.from_file('/path/to/file')
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
        TurbulentWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TurbulentWind.from_json('{ ... }')
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
        TurbulentWind
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

TurbulentWind.update_forward_refs()
