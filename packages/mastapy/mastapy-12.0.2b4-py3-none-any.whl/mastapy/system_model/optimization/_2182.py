﻿"""_2182.py

ConicalGearOptimizationStep
"""


from mastapy.system_model.optimization import _2189
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_OPTIMIZATION_STEP = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'ConicalGearOptimizationStep')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearOptimizationStep',)


class ConicalGearOptimizationStep(_2189.OptimizationStep):
    """ConicalGearOptimizationStep

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_OPTIMIZATION_STEP

    def __init__(self, instance_to_wrap: 'ConicalGearOptimizationStep.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
