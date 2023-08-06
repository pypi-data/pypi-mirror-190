﻿"""_4622.py

SpiralBevelGearMeshModalAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2275
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6880
from mastapy.system_model.analyses_and_results.system_deflections import _2753
from mastapy.system_model.analyses_and_results.modal_analyses import _4530
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'SpiralBevelGearMeshModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshModalAnalysis',)


class SpiralBevelGearMeshModalAnalysis(_4530.BevelGearMeshModalAnalysis):
    """SpiralBevelGearMeshModalAnalysis

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2275.SpiralBevelGearMesh':
        """SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6880.SpiralBevelGearMeshLoadCase':
        """SpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2753.SpiralBevelGearMeshSystemDeflection':
        """SpiralBevelGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
