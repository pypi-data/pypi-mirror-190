
import numpy

from FiberFusing.baseclass import BaseFused
from FiberFusing.rings import FiberRing


class Fused3(BaseFused):
    def __init__(self,
                 fiber_radius: float,
                 fusion_degree: float,
                 index: float,
                 core_position_scrambling: float = 0):

        super().__init__(
            fiber_radius=fiber_radius,
            fusion_degree=fusion_degree,
            index=index,
            core_position_scrambling=core_position_scrambling
        )

        assert 0 <= fusion_degree <= 1, "fusion_degree degree has to be in the range [0, 1]"

        Ring0 = FiberRing(
            angle_list=numpy.linspace(0, 360, 3, endpoint=False),
            fusion_degree=self.fusion_degree,
            fiber_radius=self.fiber_radius
        )

        self.add_fiber_ring(Ring0)

        self.Object = self.compute_optimize_geometry()


if __name__ == '__main__':
    a = Fused3(fiber_radius=60, fusion_degree=0.3, index=1)
    a.plot(show_fibers=True, show_added=True, show_removed=True).show()
