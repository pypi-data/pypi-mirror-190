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

from dnv_bladed_models.wind_direction_shear_variation import WindDirectionShearVariation


class PresetWindDirectionShearTransient_VariationShapeEnum(str, Enum):
    FULL = "FULL"
    HALF = "HALF"
    IEC_2 = "IEC-2"

class PresetWindDirectionShearTransient(WindDirectionShearVariation, DirectionShearVariationType='PresetTransient'):
    """PresetWindDirectionShearTransient - A preset transient in the vertical direction shear (wind veer).  This is a linear relationship between the height and the local direction, with the direction being its nominal value at the reference height.

    Attributes:
        - DirectionShearAtStart: float => A number representing an angle varying by a length.  The SI units for angle per length radians per metre.
        - AmplitudeOfVariation: float => A number representing an angle varying by a length.  The SI units for angle per length radians per metre.
        - StartTime: float => A number representing a time.  The SI units for time are seconds.
        - DurationOfVariation: float => A number representing a time.  The SI units for time are seconds.
        - VariationShape: PresetWindDirectionShearTransient_VariationShapeEnum => The shape of the transient.  This can either be a half-cycle (where the shear remains at the initial value plus the amplitude after the transient has been completed) or a full-cycle (where the shear returns to its original value).
        - DirectionShearVariationType: str [Read-only] => Allows the schema to identify the type of the object.  For this type of object, this must always be set to &#39;PresetTransient&#39;
    """

    DirectionShearAtStart: Optional[float] = Field(alias="DirectionShearAtStart", default=None)
    AmplitudeOfVariation: Optional[float] = Field(alias="AmplitudeOfVariation", default=None)
    StartTime: Optional[float] = Field(alias="StartTime", default=None)
    DurationOfVariation: Optional[float] = Field(alias="DurationOfVariation", default=None)
    VariationShape: Optional[PresetWindDirectionShearTransient_VariationShapeEnum] = Field(alias="VariationShape", default=None)
    DirectionShearVariationType: Optional[str] = Field(alias="DirectionShearVariationType", default='PresetTransient', allow_mutation=False)

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
        PresetWindDirectionShearTransient
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PresetWindDirectionShearTransient.from_file('/path/to/file')
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
        PresetWindDirectionShearTransient
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PresetWindDirectionShearTransient.from_json('{ ... }')
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
        PresetWindDirectionShearTransient
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

PresetWindDirectionShearTransient.update_forward_refs()
