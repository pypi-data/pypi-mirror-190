﻿"""_4473.py

PulleyCompoundParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2541, _2538
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4344
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4424
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PulleyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundParametricStudyTool',)


class PulleyCompoundParametricStudyTool(_4424.CouplingHalfCompoundParametricStudyTool):
    """PulleyCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'PulleyCompoundParametricStudyTool.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_4344.PulleyParametricStudyTool]':
        """List[PulleyParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4344.PulleyParametricStudyTool]':
        """List[PulleyParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
