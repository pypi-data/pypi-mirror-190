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

from dnv_bladed_models.signal_properties_acceleration import SignalPropertiesAcceleration

from dnv_bladed_models.signal_properties_angle import SignalPropertiesAngle

from dnv_bladed_models.signal_properties_angular_acceleration import SignalPropertiesAngularAcceleration

from dnv_bladed_models.signal_properties_angular_velocity import SignalPropertiesAngularVelocity

from dnv_bladed_models.signal_properties_force import SignalPropertiesForce

from dnv_bladed_models.signal_properties_length import SignalPropertiesLength

from dnv_bladed_models.signal_properties_moment import SignalPropertiesMoment

from dnv_bladed_models.signal_properties_power import SignalPropertiesPower

from dnv_bladed_models.signal_properties_velocity import SignalPropertiesVelocity


class MeasuredSignalProperties(Dnv):
    """MeasuredSignalProperties - The noise and transducer properties for those signals representing values coming from a physical sensor.

    Attributes:
        - RandomNumberSeed: int => A seed for the random number generator to ensure that subsequent runs have identical noise signatures.
        - TurnOffNoise: bool => This allows the noise to be turned off globally.  Note: this turns off noise, but keeps discretisation, sampling time, faults and transducer behaviour.
        - ShaftPowerSignals: SignalPropertiesPower 
        - RotorSpeedSignals: SignalPropertiesAngularVelocity 
        - ElectricalPowerOutputSignals: SignalPropertiesPower 
        - GeneratorSpeedSignals: SignalPropertiesAngularVelocity 
        - GeneratorTorqueSignals: SignalPropertiesMoment 
        - YawBearingAngularPositionSignals: SignalPropertiesAngle 
        - YawBearingAngularVelocitySignals: SignalPropertiesAngularVelocity 
        - YawBearingAngularAccelerationSignals: SignalPropertiesAngularAcceleration 
        - YawMotorRateSignals: SignalPropertiesAngularVelocity 
        - YawErrorSignals: SignalPropertiesAngle 
        - NacelleAngleFromNorthSignals: SignalPropertiesAngle 
        - TowerTopForeAftAccelerationSignals: SignalPropertiesAcceleration 
        - TowerTopSideSideAccelerationSignals: SignalPropertiesAcceleration 
        - ShaftTorqueSignals: SignalPropertiesMoment 
        - YawBearingMySignals: SignalPropertiesMoment 
        - YawBearingMzSignals: SignalPropertiesMoment 
        - NacelleRollAngleSignals: SignalPropertiesAngle 
        - NacelleNoddingAngleSignals: SignalPropertiesAngle 
        - NacelleRollAccelerationSignals: SignalPropertiesAngularAcceleration 
        - NacelleNoddingAccelerationSignals: SignalPropertiesAngularAcceleration 
        - NacelleYawAccelerationSignals: SignalPropertiesAngularAcceleration 
        - RotorAzimuthAngleSignals: SignalPropertiesAngle 
        - NominalHubFlowSpeedSignals: SignalPropertiesVelocity 
        - RotatingHubMySignals: SignalPropertiesMoment 
        - RotatingHubMzSignals: SignalPropertiesMoment 
        - FixedHubMySignals: SignalPropertiesMoment 
        - FixedHubMzSignals: SignalPropertiesMoment 
        - FixedHubFxSignals: SignalPropertiesForce 
        - FixedHubFySignals: SignalPropertiesForce 
        - FixedHubFzSignals: SignalPropertiesForce 
        - PitchAngleSignals: SignalPropertiesAngle 
        - PitchRateSignals: SignalPropertiesAngularVelocity 
        - PitchActuatorTorqueSignals: SignalPropertiesMoment 
        - PitchBearingFrictionSignals: SignalPropertiesMoment 
        - PitchBearingStictionSignals: SignalPropertiesMoment 
        - BladeOutOfPlaneBendingMomentSignals: SignalPropertiesMoment 
        - BladeInPlaneBendingMomentSignals: SignalPropertiesMoment 
        - PitchBearingMxSignals: SignalPropertiesMoment 
        - PitchBearingMySignals: SignalPropertiesMoment 
        - PitchBearingMzSignals: SignalPropertiesMoment 
        - PitchBearingRadialForceSignals: SignalPropertiesForce 
        - PitchBearingAxialForceSignals: SignalPropertiesForce 
        - PitchBearingFxSignals: SignalPropertiesForce 
        - PitchBearingFySignals: SignalPropertiesForce 
        - BladeStationWindSpeedSignals: SignalPropertiesVelocity 
        - BladeStationAngleOfAttackSignals: SignalPropertiesAngle 
        - AileronAngleSignals: SignalPropertiesAngle 
        - AileronRateSignals: SignalPropertiesAngularVelocity 
        - BladeStationPositionXSignals: SignalPropertiesLength 
        - BladeStationPositionYSignals: SignalPropertiesLength 
        - BladeStationPositionZSignals: SignalPropertiesLength 
        - BladeStationPositionXRotationSignals: SignalPropertiesAngle 
        - BladeStationPositionYRotationSignals: SignalPropertiesAngle 
        - BladeStationPositionZRotationSignals: SignalPropertiesAngle 
        - LidarBeamFocalPointVelocitySignals: SignalPropertiesVelocity 
    """

    RandomNumberSeed: Optional[int] = Field(alias="RandomNumberSeed", default=0)
    TurnOffNoise: Optional[bool] = Field(alias="TurnOffNoise", default=False)
    ShaftPowerSignals: Optional[SignalPropertiesPower] = Field(alias="ShaftPowerSignals", default=None)
    RotorSpeedSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="RotorSpeedSignals", default=None)
    ElectricalPowerOutputSignals: Optional[SignalPropertiesPower] = Field(alias="ElectricalPowerOutputSignals", default=None)
    GeneratorSpeedSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="GeneratorSpeedSignals", default=None)
    GeneratorTorqueSignals: Optional[SignalPropertiesMoment] = Field(alias="GeneratorTorqueSignals", default=None)
    YawBearingAngularPositionSignals: Optional[SignalPropertiesAngle] = Field(alias="YawBearingAngularPositionSignals", default=None)
    YawBearingAngularVelocitySignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="YawBearingAngularVelocitySignals", default=None)
    YawBearingAngularAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="YawBearingAngularAccelerationSignals", default=None)
    YawMotorRateSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="YawMotorRateSignals", default=None)
    YawErrorSignals: Optional[SignalPropertiesAngle] = Field(alias="YawErrorSignals", default=None)
    NacelleAngleFromNorthSignals: Optional[SignalPropertiesAngle] = Field(alias="NacelleAngleFromNorthSignals", default=None)
    TowerTopForeAftAccelerationSignals: Optional[SignalPropertiesAcceleration] = Field(alias="TowerTopForeAftAccelerationSignals", default=None)
    TowerTopSideSideAccelerationSignals: Optional[SignalPropertiesAcceleration] = Field(alias="TowerTopSideSideAccelerationSignals", default=None)
    ShaftTorqueSignals: Optional[SignalPropertiesMoment] = Field(alias="ShaftTorqueSignals", default=None)
    YawBearingMySignals: Optional[SignalPropertiesMoment] = Field(alias="YawBearingMySignals", default=None)
    YawBearingMzSignals: Optional[SignalPropertiesMoment] = Field(alias="YawBearingMzSignals", default=None)
    NacelleRollAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="NacelleRollAngleSignals", default=None)
    NacelleNoddingAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="NacelleNoddingAngleSignals", default=None)
    NacelleRollAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="NacelleRollAccelerationSignals", default=None)
    NacelleNoddingAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="NacelleNoddingAccelerationSignals", default=None)
    NacelleYawAccelerationSignals: Optional[SignalPropertiesAngularAcceleration] = Field(alias="NacelleYawAccelerationSignals", default=None)
    RotorAzimuthAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="RotorAzimuthAngleSignals", default=None)
    NominalHubFlowSpeedSignals: Optional[SignalPropertiesVelocity] = Field(alias="NominalHubFlowSpeedSignals", default=None)
    RotatingHubMySignals: Optional[SignalPropertiesMoment] = Field(alias="RotatingHubMySignals", default=None)
    RotatingHubMzSignals: Optional[SignalPropertiesMoment] = Field(alias="RotatingHubMzSignals", default=None)
    FixedHubMySignals: Optional[SignalPropertiesMoment] = Field(alias="FixedHubMySignals", default=None)
    FixedHubMzSignals: Optional[SignalPropertiesMoment] = Field(alias="FixedHubMzSignals", default=None)
    FixedHubFxSignals: Optional[SignalPropertiesForce] = Field(alias="FixedHubFxSignals", default=None)
    FixedHubFySignals: Optional[SignalPropertiesForce] = Field(alias="FixedHubFySignals", default=None)
    FixedHubFzSignals: Optional[SignalPropertiesForce] = Field(alias="FixedHubFzSignals", default=None)
    PitchAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="PitchAngleSignals", default=None)
    PitchRateSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="PitchRateSignals", default=None)
    PitchActuatorTorqueSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchActuatorTorqueSignals", default=None)
    PitchBearingFrictionSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingFrictionSignals", default=None)
    PitchBearingStictionSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingStictionSignals", default=None)
    BladeOutOfPlaneBendingMomentSignals: Optional[SignalPropertiesMoment] = Field(alias="BladeOutOfPlaneBendingMomentSignals", default=None)
    BladeInPlaneBendingMomentSignals: Optional[SignalPropertiesMoment] = Field(alias="BladeInPlaneBendingMomentSignals", default=None)
    PitchBearingMxSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingMxSignals", default=None)
    PitchBearingMySignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingMySignals", default=None)
    PitchBearingMzSignals: Optional[SignalPropertiesMoment] = Field(alias="PitchBearingMzSignals", default=None)
    PitchBearingRadialForceSignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingRadialForceSignals", default=None)
    PitchBearingAxialForceSignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingAxialForceSignals", default=None)
    PitchBearingFxSignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingFxSignals", default=None)
    PitchBearingFySignals: Optional[SignalPropertiesForce] = Field(alias="PitchBearingFySignals", default=None)
    BladeStationWindSpeedSignals: Optional[SignalPropertiesVelocity] = Field(alias="BladeStationWindSpeedSignals", default=None)
    BladeStationAngleOfAttackSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationAngleOfAttackSignals", default=None)
    AileronAngleSignals: Optional[SignalPropertiesAngle] = Field(alias="AileronAngleSignals", default=None)
    AileronRateSignals: Optional[SignalPropertiesAngularVelocity] = Field(alias="AileronRateSignals", default=None)
    BladeStationPositionXSignals: Optional[SignalPropertiesLength] = Field(alias="BladeStationPositionXSignals", default=None)
    BladeStationPositionYSignals: Optional[SignalPropertiesLength] = Field(alias="BladeStationPositionYSignals", default=None)
    BladeStationPositionZSignals: Optional[SignalPropertiesLength] = Field(alias="BladeStationPositionZSignals", default=None)
    BladeStationPositionXRotationSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationPositionXRotationSignals", default=None)
    BladeStationPositionYRotationSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationPositionYRotationSignals", default=None)
    BladeStationPositionZRotationSignals: Optional[SignalPropertiesAngle] = Field(alias="BladeStationPositionZRotationSignals", default=None)
    LidarBeamFocalPointVelocitySignals: Optional[SignalPropertiesVelocity] = Field(alias="LidarBeamFocalPointVelocitySignals", default=None)

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
        MeasuredSignalProperties
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MeasuredSignalProperties.from_file('/path/to/file')
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
        MeasuredSignalProperties
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MeasuredSignalProperties.from_json('{ ... }')
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
        MeasuredSignalProperties
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

MeasuredSignalProperties.update_forward_refs()
