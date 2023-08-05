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


class DynamicWake_AreaAveragingMethodEnum(str, Enum):
    OVER_ANNULUS = "OVER_ANNULUS"
    NONE = "NONE"

class DynamicWake_DynamicWakeTypeEnum(str, Enum):
    OYE_DYNAMIC_WAKE = "OyeDynamicWake"
    PITT_AND_PETERS_MODEL = "PittAndPetersModel"
    FREE_FLOW_MODEL = "FreeFlowModel"
    EQUILIBRIUM_WAKE_MODEL = "EquilibriumWakeModel"

class DynamicWake(Dnv):
    """DynamicWake - Common properties for all dynamic wake models.

    Attributes:
        - AreaAveragingMethod: DynamicWake_AreaAveragingMethodEnum => With the \&quot;over annulus\&quot; method, the dynamic wake is calculated over the entire annular ring.  Induced velocities are averaged over the number of blades.  If \&quot;none\&quot; is selected, the annulus is divided into segments to which separate dynamic wakes are applied.
        - DynamicWakeType: DynamicWake_DynamicWakeTypeEnum => Allows the schema to identify the type of the object.
        
    This class is an abstraction, with the following concrete implementations:
        - EquilibriumWakeModel
        - FreeFlowModel
        - OyeDynamicWake
        - PittAndPetersModel
    """

    AreaAveragingMethod: Optional[DynamicWake_AreaAveragingMethodEnum] = Field(alias="AreaAveragingMethod", default='OVER_ANNULUS')
    DynamicWakeType: Optional[DynamicWake_DynamicWakeTypeEnum] = Field(alias="DynamicWakeType", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass

    _subtypes_ = dict()

    def __init_subclass__(cls, DynamicWakeType=None):
        cls._subtypes_[DynamicWakeType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._convert_to_real_type_

    @classmethod
    def _convert_to_real_type_(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("DynamicWakeType")

            if data_type is None:
                raise ValueError("Missing 'DynamicWakeType' in DynamicWake")

            sub = cls._subtypes_.get(data_type)

            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'DynamicWake'")

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
        DynamicWake
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DynamicWake.from_file('/path/to/file')
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
        DynamicWake
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DynamicWake.from_json('{ ... }')
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
        DynamicWake
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

DynamicWake.update_forward_refs()
