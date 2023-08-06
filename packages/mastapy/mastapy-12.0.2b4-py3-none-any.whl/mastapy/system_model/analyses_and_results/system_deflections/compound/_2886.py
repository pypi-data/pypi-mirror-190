﻿"""_2886.py

PulleyCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2541, _2538
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.system_deflections import _2739
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2836
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PulleyCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundSystemDeflection',)


class PulleyCompoundSystemDeflection(_2836.CouplingHalfCompoundSystemDeflection):
    """PulleyCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _PULLEY_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'PulleyCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2541.Pulley':
        """Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2541.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_2739.PulleySystemDeflection]':
        """List[PulleySystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2739.PulleySystemDeflection]':
        """List[PulleySystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
