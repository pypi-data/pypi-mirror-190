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

from dnv_bladed_models.emergency_stop_button import EmergencyStopButton

from dnv_bladed_models.generator_overpower import GeneratorOverpower

from dnv_bladed_models.generator_overspeed import GeneratorOverspeed

from dnv_bladed_models.generator_short_circuit import GeneratorShortCircuit

from dnv_bladed_models.nacelle_vibration import NacelleVibration

from dnv_bladed_models.rotor_overspeed import RotorOverspeed

from dnv_bladed_models.safety_system_circuit import SafetySystemCircuit


class SafetySystem(Dnv):
    """SafetySystem - The definition of the turbine&#39;s safety system.  This supersedes the turbine&#39;s controller requests.

    Attributes:
        - Circuits: Dict[str, SafetySystemCircuit] => A library of the available safety system circuits.  These can be referenced by the individual trips.
        - GeneratorOverspeed: GeneratorOverspeed 
        - RotorOverspeed: RotorOverspeed 
        - GeneratorOverpower: GeneratorOverpower 
        - NacelleVibration: NacelleVibration 
        - GeneratorShortCircuit: GeneratorShortCircuit 
        - EmergencyStopButton: EmergencyStopButton 
        - OnlyActivateOnceLoggingHasCommenced: bool => If true, the safety system will be inactivated during the lead in time when there is no logging.
    """

    Circuits: Optional[Dict[str, SafetySystemCircuit]] = Field(alias="Circuits", default=dict())
    GeneratorOverspeed: Optional[GeneratorOverspeed] = Field(alias="GeneratorOverspeed", default=None)
    RotorOverspeed: Optional[RotorOverspeed] = Field(alias="RotorOverspeed", default=None)
    GeneratorOverpower: Optional[GeneratorOverpower] = Field(alias="GeneratorOverpower", default=None)
    NacelleVibration: Optional[NacelleVibration] = Field(alias="NacelleVibration", default=None)
    GeneratorShortCircuit: Optional[GeneratorShortCircuit] = Field(alias="GeneratorShortCircuit", default=None)
    EmergencyStopButton: Optional[EmergencyStopButton] = Field(alias="EmergencyStopButton", default=None)
    OnlyActivateOnceLoggingHasCommenced: Optional[bool] = Field(alias="OnlyActivateOnceLoggingHasCommenced", default=None)

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
        SafetySystem
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SafetySystem.from_file('/path/to/file')
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
        SafetySystem
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SafetySystem.from_json('{ ... }')
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
        SafetySystem
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

SafetySystem.update_forward_refs()
