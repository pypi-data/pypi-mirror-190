import numpy

from FiberFusing.baseclass import BaseFused
from FiberFusing.rings import FiberRing


class Fused19(BaseFused):
    def __init__(self,
                 fiber_radius: float,
                 fusion_degree: float,
                 index: float,
                 core_position_scrambling: float = 0):

        super().__init__(
            fiber_radius=fiber_radius,
            fusion_degree=fusion_degree,
            angle_list=numpy.linspace(0, 360, 6, endpoint=False),
            index=index,
            core_position_scrambling=core_position_scrambling
        )

        Ring0 = FiberRing(
            angle_list=numpy.linspace(0, 360, 6, endpoint=False), 
            fusion_degree=self.fusion_degree, 
            fiber_radius=self.fiber_radius
        )

        Ring1 = FiberRing(
            angle_list=[0], 
            fusion_degree=self.fusion_degree, 
            fiber_radius=self.fiber_radius
        )

        Ring2 = FiberRing(
            angle_list=numpy.linspace(0, 360, 12, endpoint=False) + 180 / 12, 
            fusion_degree=self.fusion_degree, 
            fiber_radius=self.fiber_radius
        )

        self.add_fiber_ring(Ring0, Ring1, Ring2)

        self.Object = self.compute_optimize_geometry()


if __name__ == '__main__':
    a = Fused19(fiber_radius=62.5, fusion_degree=0.6, index=1)
    a.Plot(Fibers=False, Added=True, Removed=False, Virtual=False, Mask=False).Show()
