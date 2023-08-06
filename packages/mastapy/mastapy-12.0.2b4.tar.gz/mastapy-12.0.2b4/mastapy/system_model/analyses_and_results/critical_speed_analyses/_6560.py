﻿"""_6560.py

PulleyCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.couplings import _2541, _2538
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6866, _6782
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6509
from mastapy._internal.python_net import python_net_import

_PULLEY_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'PulleyCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCriticalSpeedAnalysis',)


class PulleyCriticalSpeedAnalysis(_6509.CouplingHalfCriticalSpeedAnalysis):
    """PulleyCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _PULLEY_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'PulleyCriticalSpeedAnalysis.TYPE'):
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
    def component_load_case(self) -> '_6866.PulleyLoadCase':
        """PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        if _6866.PulleyLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to PulleyLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
