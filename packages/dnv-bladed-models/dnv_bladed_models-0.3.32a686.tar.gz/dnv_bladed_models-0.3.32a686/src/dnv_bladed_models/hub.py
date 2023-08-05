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

from dnv_bladed_models.blade_mounting_on_rotor import BladeMountingOnRotor

from dnv_bladed_models.component import Component

from dnv_bladed_models.connectable_node import ConnectableNode

from dnv_bladed_models.extension_pieces import ExtensionPieces

from dnv_bladed_models.hub_mass_properties import HubMassProperties

from dnv_bladed_models.hub_output_group import HubOutputGroup

from dnv_bladed_models.low_speed_shaft import LowSpeedShaft

from dnv_bladed_models.spinner import Spinner


class Hub_RotationDirectionEnum(str, Enum):
    CLOCKWISE_VIEWED_FROM_FRONT = "CLOCKWISE_VIEWED_FROM_FRONT"
    ANTICLOCKWISE_VIEWED_FROM_FRONT = "ANTICLOCKWISE_VIEWED_FROM_FRONT"

class Hub_UpwindOrDownwindEnum(str, Enum):
    UPWIND = "UPWIND"
    DOWNWIND = "DOWNWIND"

class Hub(Component):
    """Hub - The common properties shared by all hubs.

    Attributes:
        - RotationDirection: Hub_RotationDirectionEnum => The rotational sense of rotor when viewed from upwind.
        - UpwindOrDownwind: Hub_UpwindOrDownwindEnum => Whether the turbine is an upwind turbine (where the rotor is upwind of the nacelle) or a downwind turbine (where the rotor is downwind of the nacelle).
        - BladeMounting: BladeMountingOnRotor 
        - LowSpeedShaft: LowSpeedShaft 
        - ExtensionPieces: ExtensionPieces 
        - MassProperties: HubMassProperties 
        - Spinner: Spinner 
        - ConnectableNodes: Dict[str, ConnectableNode] => A declaration of what nodes can be connected to.
        - OutputGroups: Dict[str, HubOutputGroup] => The hub loads to be output in the simulations.
    """

    RotationDirection: Optional[Hub_RotationDirectionEnum] = Field(alias="RotationDirection", default=None)
    UpwindOrDownwind: Optional[Hub_UpwindOrDownwindEnum] = Field(alias="UpwindOrDownwind", default=None)
    BladeMounting: Optional[BladeMountingOnRotor] = Field(alias="BladeMounting", default=None)
    LowSpeedShaft: Optional[LowSpeedShaft] = Field(alias="LowSpeedShaft", default=None)
    ExtensionPieces: Optional[ExtensionPieces] = Field(alias="ExtensionPieces", default=None)
    MassProperties: Optional[HubMassProperties] = Field(alias="MassProperties", default=None)
    Spinner: Optional[Spinner] = Field(alias="Spinner", default=None)
    ConnectableNodes: Optional[Dict[str, ConnectableNode]] = Field(alias="ConnectableNodes", default=dict())
    OutputGroups: Optional[Dict[str, HubOutputGroup]] = Field(alias="OutputGroups", default=dict())

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
        Hub
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Hub.from_file('/path/to/file')
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
        Hub
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Hub.from_json('{ ... }')
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
        Hub
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

Hub.update_forward_refs()
