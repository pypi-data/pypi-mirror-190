"""
2x2 Coupler
===========
"""

# %%
# Importing the package dependencies: FiberFusing, PyOptik [optional]
from FiberFusing import Geometry, Fused3, Circle, BackGround
from SuPyMode.solver import SuPySolver
from SuPyMode.profiles import AlphaProfile


# %%
# Generating the fiber structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Here we make use of the FiberFusing to generate a fiber structure that we use
# as the cladding. The refractive index of the strcture is defined using PyOptik.
wavelength = 1.55e-6

index = 1.4444

air = BackGround(index=1)

clad = Fused3(fiber_radius=62.5e-6, fusion_degree=0.99, index=index)

clad.plot().show()

# %%
# Creating the geometry rasterization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The cladding being defined we create the cores that are distributed at
# each (virtual) center of the cladding.
# All the components: air -- cladding -- cores, are inputed into a geometry class
# that will generate the mesh which will be used in the finit-difference matrix.
cores = [Circle(position=fiber.core, radius=4.1e-6, index=index + 0.005) for fiber in clad.fiber_list]

geometry = Geometry(
    background=air,
    structures=[clad, *cores],
    x_bounds='auto',
    y_bounds='auto',
    n=60,
    index_scrambling=1e-6,
    gaussian_filter=0.2
)

# _ = geometry.plot().show()

# %%
# We here create the solver class and generate the superset which
# will contains the supermodes to be computed.
solver = SuPySolver(geometry=geometry, tolerance=1e-8, max_iter=10000)

solver.init_superset(wavelength=wavelength, n_step=500, itr_i=1.0, itr_f=0.05)


# %%
# We now add supermodes for different type of attributes such as symmetries.
# By default the solver assume no symmetries in the system.
_ = solver.add_modes(
    sorting='field',
    boundaries={'right': 'zero', 'left': 'zero', 'top': 'zero', 'bottom': 'zero'},
    n_computed_mode=8,
    n_sorted_mode=4
)

# %%
# The modes are now computed [can take a few minutes], the modes are concatenated
# in a superset class that we can access with the get_set() function. This class
# can be used to analyse the data
superset = solver.get_set()

# %%
# Generating the z-profile of the coupler
profile = AlphaProfile(
    alpha=0, 
    x_0=315 * 0.02 * 1e-3, 
    rho_0=60e-6, 
    L0=3 * 1e-3,
    name='test profile'
)

profile.add_taper_segment(
    alpha=0.2, 
    x_0=2020 * 0.02 * 1e-3,
    L0=10 * 1e-3
)

profile.initialize()

profile.plot().show()


# %%
# Field computation: :math:`E_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='field', itr_list=[1.0, 0.05]).show()

# %%
# After mode visualization we can name them for an easier further analyze.
# This step is, however, not mandatory.
_ = superset.name_supermodes('LP01', 'LP11_v', 'LP21', 'LP11_h')

# %%
# Effective index: :math:`n^{eff}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='index').show()

# %%
# Modal coupling: :math:`C_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='coupling', mode_selection='all').show()

# %%
# Adiabatic criterion: :math:`\tilde{C}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='adiabatic', mode_selection='all', add_profile=[profile]).show()
