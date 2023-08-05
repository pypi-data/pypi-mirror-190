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


class DynamicStall_DynamicStallTypeEnum(str, Enum):
    OYE_MODEL = "OyeModel"
    INCOMPRESSIBLE_BEDDOES_LEISHMAN_MODEL = "IncompressibleBeddoesLeishmanModel"
    COMPRESSIBLE_BEDDOES_LEISHMAN_MODEL = "CompressibleBeddoesLeishmanModel"

class DynamicStall(Dnv):
    """DynamicStall - The common properties of all of the dynamic stall models.

    Attributes:
        - UseDynamicPitchingMomentCoefficient: bool => If true, the dynamic pitching moment coefficient will be used.  This option is enabled by default.  It is not recommended to disable this option for blades with a torsional degree of freedom because the so-called &#39;pitch- rate damping&#39; term of the moment coefficient is typically important to keep the blade torsional mode stable.
        - StartingRadius: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - EndingRadius: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - SeparationTimeConstant: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - UseAveragedLocalTangentMethod: bool => If true, the averaged polar gradient is used to reconstruct the inviscid polar data.  The averaging is performed between AoA&#x3D;-2 deg to AoA&#x3D;7 deg at 0.5 deg intervals.  This approach is more suitable for polar data sets where the lift coefficient slope is not straight around 0 deg angle of attack.  It is recommended to activate this option for more accurate computations.  This option is turned on by default. Switch off for obtaining consistent results with Bladed 4.12 and earlier.
        - DynamicStallType: DynamicStall_DynamicStallTypeEnum => Allows the schema to identify the type of the object.
        
    This class is an abstraction, with the following concrete implementations:
        - CompressibleBeddoesLeishmanModel
        - IncompressibleBeddoesLeishmanModel
        - OyeModel
    """

    UseDynamicPitchingMomentCoefficient: Optional[bool] = Field(alias="UseDynamicPitchingMomentCoefficient", default=True)
    StartingRadius: Optional[float] = Field(alias="StartingRadius", default=None)
    EndingRadius: Optional[float] = Field(alias="EndingRadius", default=None)
    SeparationTimeConstant: Optional[float] = Field(alias="SeparationTimeConstant", default=None)
    UseAveragedLocalTangentMethod: Optional[bool] = Field(alias="UseAveragedLocalTangentMethod", default=True)
    DynamicStallType: Optional[DynamicStall_DynamicStallTypeEnum] = Field(alias="DynamicStallType", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass

    _subtypes_ = dict()

    def __init_subclass__(cls, DynamicStallType=None):
        cls._subtypes_[DynamicStallType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_real_type_

    @classmethod
    def _convert_to_real_type_(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("DynamicStallType")

            if data_type is None:
                raise ValueError("Missing 'DynamicStallType' in DynamicStall")

            sub = cls._subtypes_.get(data_type)

            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'DynamicStall'")

            return sub(**data)

        return data

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
        DynamicStall
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DynamicStall.from_file('/path/to/file')
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
        DynamicStall
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DynamicStall.from_json('{ ... }')
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
        DynamicStall
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

DynamicStall.update_forward_refs()
