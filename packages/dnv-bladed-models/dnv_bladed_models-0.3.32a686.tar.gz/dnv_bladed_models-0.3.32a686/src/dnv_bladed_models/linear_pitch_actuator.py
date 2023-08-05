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

from dnv_bladed_models.pitch_actuator import PitchActuator

from dnv_bladed_models.pitch_force_limits import PitchForceLimits

from dnv_bladed_models.response_to_demand import ResponseToDemand


class LinearPitchActuator(PitchActuator, ActuatorDriveType='LinearActuator'):
    """LinearPitchActuator - A linear pitch actuation definition.

    Attributes:
        - ForceResponse: ResponseToDemand 
        - PivotOffset: float => A number representing a length.  The SI units for length are metres.
        - PitchAngleAtMaximumTorque: float => A number representing an angle.  The SI units for angles are radians.
        - BrakeForce: float => A number representing a force.  The SI units for force are Newtons.
        - ForceLimits: PitchForceLimits 
        - BackupPowerForceLimits: PitchForceLimits 
        - RadiusOfArm: float => A number representing a length.  The SI units for length are metres.
        - ActuatorDriveType: str [Read-only] => Allows the schema to identify the type of the object.  For this type of object, this must always be set to &#39;LinearActuator&#39;
    """

    ForceResponse: Optional[ResponseToDemand] = Field(alias="ForceResponse", default=None)
    PivotOffset: Optional[float] = Field(alias="PivotOffset", default=None)
    PitchAngleAtMaximumTorque: Optional[float] = Field(alias="PitchAngleAtMaximumTorque", default=None)
    BrakeForce: Optional[float] = Field(alias="BrakeForce", default=None)
    ForceLimits: Optional[PitchForceLimits] = Field(alias="ForceLimits", default=None)
    BackupPowerForceLimits: Optional[PitchForceLimits] = Field(alias="BackupPowerForceLimits", default=None)
    RadiusOfArm: Optional[float] = Field(alias="RadiusOfArm", default=None)
    ActuatorDriveType: Optional[str] = Field(alias="ActuatorDriveType", default='LinearActuator', allow_mutation=False)

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
        LinearPitchActuator
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LinearPitchActuator.from_file('/path/to/file')
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
        LinearPitchActuator
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LinearPitchActuator.from_json('{ ... }')
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
        LinearPitchActuator
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

LinearPitchActuator.update_forward_refs()
