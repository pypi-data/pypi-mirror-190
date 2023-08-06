﻿"""_7322.py

UnbalancedMassAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2429
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6906
from mastapy.system_model.analyses_and_results.system_deflections import _2780
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7323
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'UnbalancedMassAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassAdvancedSystemDeflection',)


class UnbalancedMassAdvancedSystemDeflection(_7323.VirtualComponentAdvancedSystemDeflection):
    """UnbalancedMassAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _UNBALANCED_MASS_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'UnbalancedMassAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2429.UnbalancedMass':
        """UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6906.UnbalancedMassLoadCase':
        """UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2780.UnbalancedMassSystemDeflection]':
        """List[UnbalancedMassSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
