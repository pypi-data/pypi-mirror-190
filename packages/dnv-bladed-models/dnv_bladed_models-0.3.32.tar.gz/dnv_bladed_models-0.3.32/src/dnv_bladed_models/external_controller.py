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


class ExternalController_CallingConventionEnum(str, Enum):
    CDECL = "__cdecl"
    STDCALL = "__stdcall"

class ExternalController_TimeStepMultiplierEnum(str, Enum):
    EVERY = "Every"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"
    FIFTH = "Fifth"
    SIXTH = "Sixth"
    SEVENTH = "Seventh"
    EIGTH = "Eigth"
    NINTH = "Ninth"
    TENTH = "Tenth"

class ExternalController(Dnv):
    """ExternalController - A definition of a single controller for the turbine.

    Attributes:
        - Filepath: str => The location of the external controller dll.
        - CallingConvention: ExternalController_CallingConventionEnum => The calling convention to be used when calling the external controller.  The default for all C-family languages is __cdecl.  The default for FORTRAN is __stdcall unless the [C] qualifier is specfied immediately after the function name.  Specifying the wrong calling convention can lead to unexplained system exceptions when attempting to call the external controller.
        - FunctionName: str => The name of the function in the dll to run.  This must satisfy the standard external controller typedef, found in the ExternalControllerApi.h.
        - PassParametersByFile: bool => If true, a file will be written containing the parameters in the above box.  The location of this file can be obtained in the external controller using the function GetInfileFilepath.  The name of this file will be \&quot;DISCON.IN\&quot; if there is only one controller, or of the pattern \&quot;DISCONn.IN\&quot;, where &#39;n&#39; is the number of the controller.  If not checked (the default), this string will be directly available using the function GetUserParameters.
        - ForceLegacy: bool => If true, only the old-style &#39;DISCON&#39; function will be looked for in the controller, and raise an error if it cannot be found.  This is only used for testing legacy controllers where both CONTROLLER and DISCON functions are both defined, but the DISCON function is required.
        - TimeStepMultiplier: ExternalController_TimeStepMultiplierEnum => Whether the controller should be called on every discrete timestep, set above.
        - Parameters: Dict[str, Any] => JSON data that will be passed to the constructor of the external module.
        - UseFloatingPointProtection: bool => If true, this will apply floating point protection when calling the external controllers.  When the protection is on, any floating point errors are trapped and reported.  When this is switched off, the behaviour will default to that of the computer&#39;s floating point machine, but this can often be to not report the error, and to use a semi-random (but often very large) number instead of the correct result.  This can lead to unrepeatable results and numeric errors.
    """

    Filepath: Optional[str] = Field(alias="Filepath", default=None)
    CallingConvention: Optional[ExternalController_CallingConventionEnum] = Field(alias="CallingConvention", default='__cdecl')
    FunctionName: Optional[str] = Field(alias="FunctionName", default='ExternalController')
    PassParametersByFile: Optional[bool] = Field(alias="PassParametersByFile", default=False)
    ForceLegacy: Optional[bool] = Field(alias="ForceLegacy", default=False)
    TimeStepMultiplier: Optional[ExternalController_TimeStepMultiplierEnum] = Field(alias="TimeStepMultiplier", default='Every')
    Parameters: Optional[Dict[str, Any]] = Field(alias="Parameters", default=None)
    UseFloatingPointProtection: Optional[bool] = Field(alias="UseFloatingPointProtection", default=True)

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
        ExternalController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ExternalController.from_file('/path/to/file')
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
        ExternalController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ExternalController.from_json('{ ... }')
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
        ExternalController
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

ExternalController.update_forward_refs()
