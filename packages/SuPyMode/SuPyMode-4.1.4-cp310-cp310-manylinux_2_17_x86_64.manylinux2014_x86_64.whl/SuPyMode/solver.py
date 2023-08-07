#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Third-party imports
import numpy
from dataclasses import dataclass, field
from PyFinitDiff.sparse2D import FiniteDifference2D

# Local imports
from SuPyMode.superset import SuperSet
from SuPyMode.binary.CppSolver import CppSolver
from SuPyMode.binary.SuperMode import SuperMode  # It has to be imported in order for pybind11 to know the type


@dataclass()
class SuPySolver(object):
    """
    .. note::
        This solver class directly links to a c++ Eigensolver.
        It solves the eigenvalues problems for a given geometry and return a collection of SuperModes.

    """
    geometry: None = field(repr=False)
    """ geometry of the coupler structure """
    tolerance: float = 1e-5
    """ Absolute tolerance on the propagation constant computation """
    max_iter: int = 10000
    """ Maximum iteration for the c++ Eigensolver """
    accuracy: int = 2
    """ Accuracy of the finit difference methode """
    show_iteration: bool = True
    """ Print option. """
    show_eigenvalues: bool = False
    """ Print option. """

    def __post_init__(self):
        self.mode_number = 0
        self.solver_number = 0

    @property
    def descriptor(self):
        return {
            "tolerance": self.tolerance,
            "max_iter": self.max_iter,
            "accuracy": self.accuracy
        }

    @property
    def axes(self) -> object:
        return self.geometry.axes

    def get_set(self):
        return self.superset

    def _initialize_binding_(self,
                             wavelength: float,
                             n_computed_mode: int,
                             n_sorted_mode: int,
                             boundaries: dict) -> CppSolver:
        """
        Initializes the c++ binding of the class.

        :param      wavelength:       Wavelenght for the mode computation
        :type       wavelength:       float
        :param      n_computed_mode:  Number of mode that are going to be solved using the c++ solver.
        :type       n_computed_mode:  int
        :param      n_sorted_mode:    Number of mode that are outputed by the c++ solver. Has to be larger than n_computed_mode.
        :type       n_sorted_mode:    int
        :param      boundaries:       Symmetries of the finit-difference system.
        :type       boundaries:       dict

        :returns:   The cpp solver.
        :rtype:     CppSolver
        """
        mesh, gradient = self.geometry.generate_mesh()

        self.FD = FiniteDifference2D(
            n_x=self.geometry.axes.nx,
            n_y=self.geometry.axes.ny,
            dx=self.geometry.axes.dx,
            dy=self.geometry.axes.dy,
            derivative=2,
            accuracy=self.accuracy,
            boundaries=boundaries
        )

        new_array = numpy.c_[self.FD.triplet._array[:, 1],
                             self.FD.triplet._array[:, 0],
                             self.FD.triplet._array[:, 2]].T

        Solver = CppSolver(
            mesh=mesh,
            gradient=gradient.ravel(),
            finit_matrix=new_array,
            n_computed_mode=n_computed_mode,
            n_sorted_mode=n_sorted_mode,
            max_iter=self.max_iter,
            tolerance=self.tolerance,
            wavelength=wavelength,
            show_iteration=self.show_iteration,
            show_eigenvalues=self.show_eigenvalues
        )

        Solver.set_boundaries(**boundaries)

        Solver.compute_laplacian()

        return Solver

    def init_superset(self,
                      wavelength: float,
                      n_step: int = 300,
                      itr_i: float = 1.0,
                      itr_f: float = 0.1) -> None:
        """
        Initialize superset instance which contains the computed superodes.

        :param      wavelength:  Wavelenght for the mode computation
        :type       wavelength:  float
        :param      n_step:      Number of stop to iterate through the ITR (inverse taper ration) section.
        :type       n_step:      int
        :param      itr_i:       Initial value of ITR.
        :type       itr_i:       float
        :param      itr_f:       Final value of ITR.
        :type       itr_f:       float
        """
        self.wavelength = wavelength
        self.n_step = n_step
        self.itr_i = itr_i
        self.itr_f = itr_f
        self.itr_list = numpy.linspace(itr_i, itr_f, n_step)
        self.superset = SuperSet(parent_solver=self)

    def add_modes(self,
                  n_sorted_mode: int,
                  boundaries: dict,
                  sorting: str = 'index',
                  n_computed_mode: int = None,
                  alpha: float = 0.) -> None:
        """
        Adds modes to the superset instance. SuperSet is accessible through .get_set().

        :param      n_sorted_mode:    Number of mode that are outputed by the c++ solver. Has to be larger than n_computed_mode.
        :type       n_sorted_mode:    int
        :param      boundaries:       Boundaries of the finit-difference system.
        :type       boundaries:       dict
        :param      sorting:          Sorting method used to classifiy the modes ['index', 'field'].
        :type       sorting:          str
        :param      n_computed_mode:  Number of mode that are going to be solved using the c++ solver.
        :type       n_computed_mode:  int
        :param      alpha:            Initial guess for mode solving (if 0, auto evaluated).
        :type       alpha:            float
        """
        if n_computed_mode is None:
            n_computed_mode = n_sorted_mode + 2

        assert sorting.lower() in ['index', 'field'], f"Incorrect sorting method: {sorting}; Sorting can be ['Index', 'Field']"

        cpp_solver = self._initialize_binding_(
            boundaries=boundaries,
            wavelength=self.wavelength,
            n_computed_mode=n_computed_mode,
            n_sorted_mode=n_sorted_mode
        )

        cpp_solver.loop_over_itr(
            itr=self.itr_list,
            extrapolation_order=self.accuracy,
            alpha=alpha
        )

        cpp_solver.sort_modes(sorting=sorting.lower())

        cpp_solver.compute_coupling_adiabatic()

        for binding_number in range(cpp_solver.n_sorted_mode):
            self.superset.append_supermode(
                cpp_solver=cpp_solver,
                binding_number=binding_number,
                solver_number=self.solver_number,
                mode_number=self.mode_number
            )

            self.mode_number += 1

        self.solver_number += 1

# ---
