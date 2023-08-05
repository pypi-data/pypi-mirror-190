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

from dnv_bladed_models.aerodynamic_model import AerodynamicModel


class VortexLine_WakeTypeEnum(str, Enum):
    FREE_WAKE = "FreeWake"
    FIXED_WAKE = "FixedWake"

class VortexLine_CoreGrowthModelEnum(str, Enum):
    RL_MODEL = "RL_Model"
    LO_MODEL = "LO_Model"
    FIXED = "Fixed"

class VortexLine_InitialVortexCoreSizeModelEnum(str, Enum):
    RL_MODEL = "RL_Model"
    LO_MODEL = "LO_Model"
    FIXED = "Fixed"

class VortexLine(AerodynamicModel, AerodynamicModelType='VortexLine'):
    """VortexLine - The Vortex Line aerodynamic model.

    Attributes:
        - MaximumNumberofFreeWakeSteps: int => Each free wake node that is emitted from the trailing edge will be allowed a maximum number of free wake steps after it will be no longer considered in the free wake solution and convected with local wind speed and last computed induction. 
        - MaximumNumberofWakeSteps: int => Each wake node will be allowed a maximum number of steps before it is removed. This option puts an upper bound on the number of wake nodes.
        - NumberOfThreads: int => The number of parallel CPU threads used in evaluation of the Biot-Savart law.  This option is only relevant when the wake type is set to \&quot;Free Wake\&quot;.
        - VortexWakeTimeStep: float => A number representing a time.  The SI units for time are seconds.
        - WakeType: VortexLine_WakeTypeEnum => The \&quot;Free Wake\&quot; option will calculate the mutual influence of all wake elements on all wake nodes during each time step.  The \&quot;Fixed Wake\&quot; option will assume that the induced velocity in all wake nodes is equal to the average wake induced velocity at 70% blade radius.  The \&quot;Free Wake\&quot; option requires substantially more calculations to be performed, and is likely to significantly slow the analysis.
        - CoreGrowthModel: VortexLine_CoreGrowthModelEnum => The Core Growth Model.
        - InitialVortexCoreSizeModel: VortexLine_InitialVortexCoreSizeModelEnum => The intial vortex core size Model.
        - FilamentStrain: bool => The filament strain.
        - LambOseenCoreGrowthConstant: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - CoreGrowthConstant: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - RamasamyLeishmanConstant: float => A number representing a fraction, ratio, or other non-dimensionalised property.
        - AerodynamicModelType: str [Read-only] => Allows the schema to identify the type of the object.  For this type of object, this must always be set to &#39;VortexLine&#39;
    """

    MaximumNumberofFreeWakeSteps: Optional[int] = Field(alias="MaximumNumberofFreeWakeSteps", default=200)
    MaximumNumberofWakeSteps: Optional[int] = Field(alias="MaximumNumberofWakeSteps", default=10000)
    NumberOfThreads: Optional[int] = Field(alias="NumberOfThreads", default=1)
    VortexWakeTimeStep: Optional[float] = Field(alias="VortexWakeTimeStep", default=None)
    WakeType: Optional[VortexLine_WakeTypeEnum] = Field(alias="WakeType", default='FreeWake')
    CoreGrowthModel: Optional[VortexLine_CoreGrowthModelEnum] = Field(alias="CoreGrowthModel", default='RL_Model')
    InitialVortexCoreSizeModel: Optional[VortexLine_InitialVortexCoreSizeModelEnum] = Field(alias="InitialVortexCoreSizeModel", default='RL_Model')
    FilamentStrain: Optional[bool] = Field(alias="FilamentStrain", default=True)
    LambOseenCoreGrowthConstant: Optional[float] = Field(alias="LambOseenCoreGrowthConstant", default=None)
    CoreGrowthConstant: Optional[float] = Field(alias="CoreGrowthConstant", default=None)
    RamasamyLeishmanConstant: Optional[float] = Field(alias="RamasamyLeishmanConstant", default=None)
    AerodynamicModelType: Optional[str] = Field(alias="AerodynamicModelType", default='VortexLine', allow_mutation=False)

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
        VortexLine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = VortexLine.from_file('/path/to/file')
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
        VortexLine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = VortexLine.from_json('{ ... }')
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
        VortexLine
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

VortexLine.update_forward_refs()
