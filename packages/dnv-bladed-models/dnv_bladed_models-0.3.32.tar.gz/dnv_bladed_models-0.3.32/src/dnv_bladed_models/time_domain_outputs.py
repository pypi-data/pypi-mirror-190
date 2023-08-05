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

from dnv_bladed_models.outputs import Outputs

from dnv_bladed_models.selected_component_output_group import SelectedComponentOutputGroup


class TimeDomainOutputs(Outputs):
    """TimeDomainOutputs - The definition outputs to write for this simulation.

    Attributes:
        - TimeStepForOutputs: float => A number representing a time.  The SI units for time are seconds.
        - LengthOfOutputBuffer: float => A number representing a time.  The SI units for time are seconds.
        - OutputSummaryInformation: bool => If true, the summary information output group will be created.
        - OutputExternalControllers: bool => If true, the controller output group will be created.
        - OutputBuoyancyInformation: bool => If true, the buoyancy output group will be created.
        - OutputFiniteElementMatrices: bool => If true, the finite element output group will be created, providing far more detail about the finite element matrices.
        - OutputSignalProperties: bool => If true, the signal properties output group will be created.  This records the properties provided to the controller, with and without noise and other distortions.
        - OutputWakePropagation: bool => If true, the eddy viscosity propagation of the wake is output as a 2D table of relative velocity against radial position and distance travelled to a \&quot;.wake\&quot; file in the output folder.
        - OutputSoftwarePerformance: bool => If true, the software performance output group will be created.
        - OutputStateInformation: bool => If true, the integrator state output group will be created.  This can be used to help understand how efficiently the integrator is coping with the simulation.
        - OutputExternalControllerExchangeObject: bool => If true, this will output all of the values contained in the external controller interface before and after each external controller call.  This is intended to assist debugging external controllers.
        - OutputExternalControllerLegacySwapArray: bool => If true, the contents of the swap array passed to a legacy controller will be logged.  This is used only when trying to debug legacy controllers, and will not produce useful results if there is more than one legacy controller being run.
        - SelectedComponentOutputGroups: List[SelectedComponentOutputGroup] => A list of references to the OutputGroup of specific components to output.  This allows the outputs of individual components to be switched off, or chosen from an available list of output regimes.  If a component is not mentioned, it will produce outputs according to its default output group, if there is one available.
    """

    TimeStepForOutputs: Optional[float] = Field(alias="TimeStepForOutputs", default=None)
    LengthOfOutputBuffer: Optional[float] = Field(alias="LengthOfOutputBuffer", default=None)
    OutputSummaryInformation: Optional[bool] = Field(alias="OutputSummaryInformation", default=True)
    OutputExternalControllers: Optional[bool] = Field(alias="OutputExternalControllers", default=True)
    OutputBuoyancyInformation: Optional[bool] = Field(alias="OutputBuoyancyInformation", default=False)
    OutputFiniteElementMatrices: Optional[bool] = Field(alias="OutputFiniteElementMatrices", default=False)
    OutputSignalProperties: Optional[bool] = Field(alias="OutputSignalProperties", default=False)
    OutputWakePropagation: Optional[bool] = Field(alias="OutputWakePropagation", default=False)
    OutputSoftwarePerformance: Optional[bool] = Field(alias="OutputSoftwarePerformance", default=False)
    OutputStateInformation: Optional[bool] = Field(alias="OutputStateInformation", default=False)
    OutputExternalControllerExchangeObject: Optional[bool] = Field(alias="OutputExternalControllerExchangeObject", default=False)
    OutputExternalControllerLegacySwapArray: Optional[bool] = Field(alias="OutputExternalControllerLegacySwapArray", default=False)
    SelectedComponentOutputGroups: Optional[List[SelectedComponentOutputGroup]] = Field(alias="SelectedComponentOutputGroups", default=list())

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
        TimeDomainOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainOutputs.from_file('/path/to/file')
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
        TimeDomainOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainOutputs.from_json('{ ... }')
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
        TimeDomainOutputs
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

TimeDomainOutputs.update_forward_refs()
