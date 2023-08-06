#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import logging
from dataclasses import dataclass

# Third-party imports
import numpy
from itertools import combinations
from scipy.optimize import minimize_scalar

# Local imports
from MPSPlots.Render2D import Scene2D, Axis
from FiberFusing import utils
from FiberFusing.connection import Connection
from FiberFusing import buffer

logging.basicConfig(level=logging.INFO)


@dataclass
class BaseFused():
    fiber_radius: float
    """ Radius of the fiber to be used, all fibers in the structure have the same radius. """
    fusion_degree: float
    """ Value describe the fusion degree of the structure the higher the value to more fused are the fibers [0, 1]. """
    index: float
    """ Refractive index of the cladding structure. """
    tolerance_factor: float = 1e-2
    """ Tolerance on the optimization problem which aim to minimize the difference between added and removed area of the heuristic algorithm. """
    core_position_scrambling: float = 0
    """ Not implemented yet. """

    def __post_init__(self):
        self._initialize_()
        self._fiber_list = None

    def _initialize_(self):
        self._fiber_rings = []
        self.custom_fiber = []
        self._hole = None
        self._topology = None
        self._added_section = None
        self._removed_section = None
        self._fiber_centers = None
        self._core_shift = None

    @property
    def _shapely_object(self):
        return self.Object

    @property
    def bounds(self):
        return self.Object.bounds

    @property
    def fiber(self) -> list:
        return self.fiber_list

    @property
    def added_section(self) -> buffer.Polygon:
        if self._added_section is None:
            self.compute_added_section()
        return self._added_section

    @property
    def removed_section(self) -> buffer.Polygon:
        if self._removed_section is None:
            self.compute_removed_section()
        return self._removed_section

    @property
    def topology(self) -> str:
        if self._topology is None:
            self.compute_topology()
        return self._topology

    def compute_topology(self) -> None:
        Limit = []
        for connection in self.connected_fibers:
            Limit.append(connection.limit_added_area)

        OverallLimit = utils.Union(*Limit) - utils.Union(*self.fiber_list)
        self.compute_removed_section()

        self._topology = 'convex' if self.total_removed_area > OverallLimit.area else 'concave'

    def merge_connections(self) -> None:
        NewConnections = []

        for n, connection0 in enumerate(self.connected_fibers):
            for m, connection1 in enumerate(self.connected_fibers):
                if m == n:
                    continue

                union = connection1.added_section.union(connection0.added_section)

                if not union.is_empty:
                    if connection1[0] == connection0[0]:
                        Set = (connection1[1], connection0[1])
                        new = Connection(*Set, Shift=self.virtual_shift)
                        NewConnections.append(new)
                        continue

                    if connection1[1] == connection0[0]:
                        Set = (connection1[0], connection0[1])
                        new = Connection(*Set, Shift=self.virtual_shift)
                        NewConnections.append(new)
                        continue

                    if connection1[0] == connection0[1]:
                        Set = (connection1[1], connection0[0])
                        new = Connection(*Set, Shift=self.virtual_shift)
                        NewConnections.append(new)
                        continue

                    if connection1[1] == connection0[1]:
                        Set = (connection1[0], connection0[0])
                        new = Connection(*Set, Shift=self.virtual_shift)
                        NewConnections.append(new)
                        continue

    def compute_added_section(self) -> None:
        added_section = []
        for n, connection in enumerate(self.connected_fibers):
            Newadded_section = connection.added_section

            added_section.append(Newadded_section)

        self._added_section = utils.Union(*added_section) - utils.Union(*self.fiber_list)
        self._added_section.remove_non_polygon()
        self._added_section.Area = self._added_section.area
        self.total_added_area = self._added_section.area

    def compute_removed_section(self) -> None:
        removed_section = []
        for connection in self.connected_fibers:
            removed_section.append(connection.removed_section)

        self._removed_section = utils.Union(*removed_section)
        self._removed_section = self._removed_section
        self._removed_section.facecolor = 'red'
        self.total_removed_area = len(self.fiber_list) * self.fiber_list[0].area - utils.Union(*self.fiber_list).area

    def get_max_distance(self) -> float:
        return numpy.max([f.get_max_distance() for f in self.fiber_list])

    @property
    def fiber_list(self) -> list:
        if self._fiber_list is None:
            self.compute_fiber_list()
        return self._fiber_list

    def add_fiber_ring(self, *rings) -> None:
        for ring in rings:
            self._fiber_rings.append(ring)

    def add_custom_fiber(self, *fibers) -> None:
        for fiber in fibers:
            self.custom_fiber.append(fiber)

    def compute_optimize_geometry(self, bounds: tuple = None) -> buffer.Polygon:
        """
        Compute the optimized geometry such that mass is conserved. 
        Does not compute the core movment.
        
        :param      bounds:  The virtual shift boundaries
        :type       bounds:  tuple
        
        :returns:   The optimize geometry.
        :rtype:     buffer.Polygon
        """

        bounds = (0, self.fiber_radius * 1e3) if bounds is None else bounds

        self.initialize_connections()

        res = minimize_scalar(
            self.get_cost_value, 
            bounds=bounds, 
            method='bounded', 
            options={'xatol': self.fiber_radius * self.tolerance_factor}
        )

        return self.get_shifted_geometry(virtual_shift=res.x)

    def compute_core_position(self) -> None:
        """
        Optimize one round for the core positions of each connections.
        """
        for connection in self.connected_fibers:
            connection.optimize_core_position()

    def compute_fiber_list(self) -> None:
        """
        Generate the fiber list.
        """
        self._fiber_list = []

        for Ring in self._fiber_rings:
            for fiber in Ring.Fibers:
                self._fiber_list.append(fiber)

        for fiber in self.custom_fiber:
            self._fiber_list.append(fiber)

        for n, fiber in enumerate(self._fiber_list):
            fiber.name = f' fiber {n}'

    def get_shifted_geometry(self, virtual_shift: float) -> buffer.Polygon:
        """
        Returns the clad geometry for a certain shift value.

        :param      virtual_shift:  The shift value
        :type       virtual_shift:  { type_description }

        :returns:   The optimized geometry.
        :rtype:     { return_type_description }
        """
        opt_geometry = utils.Union(*self.fiber_list, self.added_section)

        self.compute_core_position()
        self.randomize_core_position()

        return opt_geometry

    def randomize_core_position(self) -> None:
        """
        Shuffle the position of the fiber cores.
        It can be used to add realism to the fusion process.
        """
        if self.core_position_scrambling != 0:
            for fiber in self._fiber_list:
                random_xy = numpy.random.rand(2) * self.core_position_scrambling
                fiber.core.translate(random_xy, in_place=True)

    def initialize_connections_cores(self) -> None:
        """
        Setup the core position for each connections.
        Initial values of the core is the center.
        """
        for connection in self.connected_fibers:
            connection[0].core = connection[0].center
            connection[1].core = connection[1].center

    def initialize_connections(self) -> None:
        """
        Generate the connections (every pair of connnected fibers).
        """
        self.connected_fibers = []

        for fibers in self.iterate_over_connected_fibers():
            connection = Connection(*fibers)
            self.connected_fibers.append(connection)

        self.initialize_connections_cores()

    def shift_connections(self, virtual_shift: float) -> None:
        """
        Set the virtual shift of the virtual circles for each of the 
        connections.
        
        :param      virtual_shift:  The shift of virtual circles
        :type       virtual_shift:  float
        """
        self.virtual_shift = virtual_shift

        for connection in self.connected_fibers:
            connection.shift = virtual_shift
            connection.topology = self.topology

        self._initialize_()

    def get_cost_value(self, virtual_shift: float) -> float:
        """
        Gets the cost value which is the difference between removed section
        and added section for a given virtual circle shift.
        
        :param      virtual_shift:  The shift of the virtual circles
        :type       virtual_shift:  float
        
        :returns:   The cost value.
        :rtype:     float
        """
        
        self.shift_connections(virtual_shift=virtual_shift)

        self.compute_added_section()
        self.compute_removed_section()
        added_section = self.total_added_area
        removed_section = self.total_removed_area
        cost = abs(added_section - removed_section)

        logging.debug(f' Fusing optimization: {virtual_shift = :.2e} \t -> \t{added_section = :.2e} \t -> {removed_section = :.2e} \t -> {cost = :.2e}')

        return cost

    def iterate_over_connected_fibers(self) -> tuple:
        """
        Just like the name implies, generator that iterate 
        over all the connected fibers.
        
        :returns:   pair of two connected fibers
        :rtype:     tuple
        """
        for fiber0, fiber1 in combinations(self.fiber_list, 2):
            if fiber0.intersection(fiber1).is_empty:
                continue
            else:
                yield fiber0, fiber1

    def get_rasterized_mesh(self, coordinate: numpy.ndarray, n_x: int, n_y: int) -> numpy.ndarray:
        Exterior = self.Object.__raster__(coordinate).reshape([n_y, n_x])

        self.Raster = Exterior

        return self.Raster

    def rotate(self, *args, **kwargs):
        """
        Rotates the full structure, including the fiber cores.
        """
        for fiber in self.fiber_list:
            fiber.rotate(*args, **kwargs, in_place=True)
            fiber.core.rotate(*args, **kwargs, in_place=True)
        self.Object = self.Object.rotate(*args, **kwargs)

    def scale_down_position(self, factor: float):
        """
        Scale down the distance between each cores.
        
        :param      factor:  The scaling factor
        :type       factor:  float
        """
        for fiber in self.fiber_list:
            fiber.scale_position(factor=factor)

    def plot(self,
             show_fibers: bool = True,
             show_added: bool = False,
             show_removed: bool = False) -> Scene2D:

        figure = Scene2D(unit_size=(6, 6))

        ax = Axis(
            row=0,
            col=0,
            x_label=r'x',
            y_label=r'y',
            show_grid=True,
            equal_limits=True,
            equal=True
        )

        figure.add_axes(ax)._generate_axis_()

        self.Object._render_(ax)
        for fiber in self.fiber_list:
            fiber._render_(ax)
            fiber.core._render_(ax)

        # if show_added:
        #     self.added_section._render_(ax)

        # if show_removed:
        #     self.removed_section._render_(ax)

        return figure


#  -
