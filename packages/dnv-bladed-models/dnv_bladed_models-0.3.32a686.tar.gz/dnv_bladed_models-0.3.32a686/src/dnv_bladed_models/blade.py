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

from dnv_bladed_models.aerofoil import Aerofoil

from dnv_bladed_models.blade_additional_inertia import BladeAdditionalInertia

from dnv_bladed_models.blade_modelling import BladeModelling

from dnv_bladed_models.blade_mounting import BladeMounting

from dnv_bladed_models.blade_output_group import BladeOutputGroup

from dnv_bladed_models.blade_section_definition import BladeSectionDefinition

from dnv_bladed_models.blade_sensor import BladeSensor

from dnv_bladed_models.component import Component


class Blade(Component, ComponentType='Blade'):
    """Blade - A blade component.

    Attributes:
        - Modelling: BladeModelling 
        - AerofoilLibrary: Dict[str, Aerofoil] => A library of Aerofoil objects, each specified with a unique keyword.  This keyword is used for referencing the item elsewhere in the model.
        - InterpolatedAerofoilLibrary: Dict[str, Dict] => A library of interpolated AerofoilLibrary, each of which has a 2D interpolation over thickness and Reynold&#39;s number.
        - AileronAerofoilLibrary: Dict[str, Dict] => A library of aileron or aileron interpolated aerofoil objects, interpolated on their deployment angle.  Each is specified with a unique keyword which is used for referencing the item elsewhere in the model.
        - Mounting: BladeMounting 
        - ToleranceForRepeatedSections: float => A number representing a length.  The SI units for length are metres.
        - SectionDefinitions: List[BladeSectionDefinition] => A list of section definitions which describle the aerodynamic and structural properties of the blade.
        - AdditionalInertia: BladeAdditionalInertia 
        - OutputGroups: Dict[str, BladeOutputGroup] => A library which contains any number of named output groups.  These can be referenced from &#39;SelectedOutputGroup&#39;
        - Sensors: Dict[str, BladeSensor] => A library of sensor objects, each specified with a unique keyword.  This keyword is used for referencing the item elsewhere in the model.
        - ComponentType: str [Read-only] => Allows the schema to identify the type of the object.  For this type of object, this must always be set to &#39;Blade&#39;
    """

    Modelling: Optional[BladeModelling] = Field(alias="Modelling", default=None)
    AerofoilLibrary: Optional[Dict[str, Aerofoil]] = Field(alias="AerofoilLibrary", default=dict())
    InterpolatedAerofoilLibrary: Optional[Dict[str, Dict]] = Field(alias="InterpolatedAerofoilLibrary", default=dict())
    AileronAerofoilLibrary: Optional[Dict[str, Dict]] = Field(alias="AileronAerofoilLibrary", default=dict())
    Mounting: Optional[BladeMounting] = Field(alias="Mounting", default=None)
    ToleranceForRepeatedSections: Optional[float] = Field(alias="ToleranceForRepeatedSections", default=None)
    SectionDefinitions: Optional[List[BladeSectionDefinition]] = Field(alias="SectionDefinitions", default=list())
    AdditionalInertia: Optional[BladeAdditionalInertia] = Field(alias="AdditionalInertia", default=None)
    OutputGroups: Optional[Dict[str, BladeOutputGroup]] = Field(alias="OutputGroups", default=dict())
    Sensors: Optional[Dict[str, BladeSensor]] = Field(alias="Sensors", default=dict())
    ComponentType: Optional[str] = Field(alias="ComponentType", default='Blade', allow_mutation=False)

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
        Blade
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Blade.from_file('/path/to/file')
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
        Blade
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Blade.from_json('{ ... }')
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
        Blade
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

Blade.update_forward_refs()
