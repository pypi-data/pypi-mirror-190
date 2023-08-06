﻿"""_7205.py

BearingAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2392
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6746
from mastapy.bearings.bearing_results import _1908, _1916, _1919
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling import (
    _1948, _1955, _1963, _1979,
    _2002
)
from mastapy.system_model.analyses_and_results.system_deflections import _2644
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7233
from mastapy._internal.python_net import python_net_import

_BEARING_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BearingAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingAdvancedSystemDeflection',)


class BearingAdvancedSystemDeflection(_7233.ConnectorAdvancedSystemDeflection):
    """BearingAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _BEARING_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'BearingAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2392.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6746.BearingLoadCase':
        """BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def duty_cycle(self) -> '_1908.LoadedBearingDutyCycle':
        """LoadedBearingDutyCycle: 'DutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DutyCycle

        if temp is None:
            return None

        if _1908.LoadedBearingDutyCycle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle to LoadedBearingDutyCycle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2644.BearingSystemDeflection]':
        """List[BearingSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[BearingAdvancedSystemDeflection]':
        """List[BearingAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
