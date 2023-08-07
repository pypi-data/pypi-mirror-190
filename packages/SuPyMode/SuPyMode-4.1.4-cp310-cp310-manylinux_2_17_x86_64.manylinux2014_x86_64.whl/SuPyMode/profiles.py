import numpy
from scipy.interpolate import interp1d

from MPSPlots.Render2D import Scene2D, Axis, Line


class GenericProfile():
    """
    Class represent the fiber structure coupler z-profile.
    This particular class is set to a Gaussian profile.
    """
    length: float
    """ Length of the fiber structure coupler """
    itr_f: float
    """ Final inverse taper ratio, per definition equal to one """
    itr_i: float = 1.0
    """ Initial inverse taper ratio, per definition equal to one """

    def __post_init__(self):
        ...

    def symmetrize_array(self, array: numpy.ndarray):
        return numpy.r_[array, array[::-1]]

    def symmetrize_distance(self, distance: numpy.ndarray):
        dz = abs(distance[0] - distance[1])
        return numpy.arange(2 * distance.size) * dz

    def symmetrize_z_r(self, z, r):
        return self.symmetrize_distance(z), self.symmetrize_array(r)


class AlphaProfile(GenericProfile):
    """
    Class represent the fiber structure coupler z-profile.
    This particular class is set to a Gaussian profile.
    """

    def __init__(self, alpha: float, x_0: float, rho_0: float, L0: float, name: str = 'profile'):
        self.taper_segment = []
        self.z_segment = []
        self.rho_w_segment = []
        self.x_0_segment = []
        self.L_segment = []
        self.rho_0 = rho_0
        self.name = name

        self.add_taper_custom_segment(
            alpha=alpha, 
            L0=L0, 
            rho_0=rho_0, 
            x_0=x_0, 
            start_z=0,
            n_point=100)

    def add_constant_segment(self, length: float, n_point: int = 100):
        """
        Add the constant section following the last section which length is to be evaluated.
        
        :param      length:   Length of the constant section to be added
        :type       length:   float
        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int
        """
        return self.add_constant_custom_section(
            length=length,
            rho=self.last_rho_z,
            start_z=self.last_z,
            n_point=n_point
        )

    def add_end_of_taper_segment(self, n_point: int = 100) -> None:
        """
        Add the constant section which length equal the final length of the 
        heating section.
        
        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int
        """
        return self.add_constant_custom_section(
            length=self.last_L / 2,
            rho=self.last_rho_z,
            start_z=self.last_z,
            n_point=n_point
        )

    def add_constant_custom_section(self, 
                                    length: float, 
                                    rho: float, 
                                    start_z: float = 0,
                                    n_point: int = 100) -> None:
        """
        Add the constant section which length, radius and start position is to be provided

        :param      length:   Length of the constant section to be added
        :type       length:   float
        :param      rho:      Radius of the constant section to be added
        :type       rho:      float   
        :param      start_z:  Initial z-position of the constant section to be added
        :type       start_z:  float        
        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int
        """
        z = numpy.linspace(0, length, n_point)

        rho_z = numpy.ones(n_point) * rho

        interpolation = interp1d(
            z + start_z, 
            rho_z, 
            bounds_error=False, 
            fill_value=0
        )

        self.taper_segment.append(interpolation)
        self.z_segment.append(length + start_z)

    def get_rho_z_from_segment(self, 
                  alpha: float, 
                  L0: float, 
                  x_0: float, 
                  rho_0: float, 
                  distance: numpy.ndarray) -> tuple:
        """
        Gets the radius as a fonction of the distance for a specific segment.,
        
        :param      alpha:    Alpha parameter which represent how the heating section changes in time
        :type       alpha:    float 
        :param      L0:       Initial length of the heating section
        :type       L0:       float   
        :param      rho_0:    The initial radius of the segment to be added
        :type       rho_0:    float  
        :param      x_0:      The total elongated lenght of the current segment to be added
        :type       x_0:      float  
        :param      distance: Array representing the z-distance.
        :type       distance: numpy.ndarray  
        """
        term0 = 2 * alpha * distance
        term2 = (1 - alpha) * L0
        term3 = -1 / (2 * alpha)

        rho_z = rho_0 * (1 + term0 / term2)**term3
        rho_w = rho_0 * (1 + alpha * x_0 / L0)**(-1 / (2 * alpha))
        l_w = L0 + alpha * x_0

        assert not numpy.any(rho_z < 0), "Negative rho value are not physical"

        return rho_z, rho_w, l_w

    def add_taper_custom_segment(self, 
                                 alpha: float, 
                                 L0: float, 
                                 rho_0: float, 
                                 x_0: float, 
                                 start_z: float = 0,
                                 n_point: int = 100):
        """
        Add a tapered section for a given alpha, L0, rho_0, x_0 and starting z position
        
        :param      alpha:    Alpha parameter which represent how the heating section changes in time
        :type       alpha:    float 
        :param      L0:       Initial length of the heating section
        :type       L0:       float   
        :param      rho_0:    The initial radius of the segment to be added
        :type       rho_0:    float  
        :param      x_0:      The total elongated lenght of the current segment to be added
        :type       x_0:      float  
        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int  
        """
        alpha = 0.0001 if alpha == 0 else alpha

        z_0 = (1 - alpha) * x_0 / 2
        distance = numpy.linspace(0, z_0, n_point)
        assert distance[0] == 0, "Computation of taper section takes z as a reference and thus has to start with 0."

        rho_z, rho_w, l_w = self.get_rho_z_from_segment(
            alpha=alpha, 
            L0=L0, 
            x_0=x_0,
            rho_0=rho_0, 
            distance=distance
        )

        interpolation = interp1d(
            distance + start_z, 
            rho_z, 
            bounds_error=False, 
            fill_value=0
        )

        self.taper_segment.append(interpolation)
        self.z_segment.append(z_0 + start_z)
        self.rho_w_segment.append(rho_w)
        self.x_0_segment.append(x_0)
        self.L_segment.append(l_w)

    @property
    def last_z(self):
        return self.z_segment[-1]

    @property
    def last_rho_z(self):
        return self.rho_w_segment[-1]

    @property
    def last_L(self):
        return self.L_segment[-1]

    @property
    def last_x_0(self):
        return self.x_0_segment[-1]

    def get_rho_z_from_segment_from_interpolation(self, z: numpy.ndarray):
        rho_z = numpy.zeros(z.size)

        for interpolation in self.taper_segment:
            rho_z += interpolation(z)

        return rho_z

    def add_taper_segment(self, 
                          alpha: float, 
                          L0: float, 
                          x_0: float, 
                          n_point: int = 100) -> None:
        """
        Add a tapered section following the previous one for a given alpha, L0, x_0.
        
        :param      alpha:    Alpha parameter which represent how the heating section changes in time
        :type       alpha:    float 
        :param      L0:       Initial length of the heating section
        :type       L0:       float   
        :param      x_0:      The total elongated lenght of the current segment to be added
        :type       x_0:      float  
        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int      
        """
        return self.add_taper_custom_segment(
            alpha=alpha, 
            L0=L0, 
            rho_0=self.last_rho_z,
            x_0=x_0,  # + self.last_x_0,
            start_z=self.last_z,
            n_point=n_point
        )

    def compute_rho_z(self) -> None:
        """
        From paper the shape of fiber tapers Timothy A. Birks

        :returns:   The rho z.
        :rtype:     numpy.ndarray
        """
        self.add_taper_custom_segment(
            alpha=-.2, 
            L0=self.L0, 
            rho_0=self.rho_0,
            x_0=self.x_0,
            start_z=0
        )

        self.add_taper_segment(
            alpha=+0.3, 
            L0=self.L0, 
            x_0=self.x_0
        )

        self.add_constant_segment(
            length=self.last_L,
        )

    def initialize(self, end_of_taper: bool = True, n_point: int = 400) -> None:
        """
        Initialize all the computation including z, rho_z, distance, length, adiabatic criterion
        
        :param      n_point:  The number of point of the z-linespace to evaluate all the parameters.
        :type       n_point:  int
        """
        if end_of_taper:
            self.add_end_of_taper_segment()

        z = numpy.linspace(0, self.last_z, n_point)

        rho_z = self.get_rho_z_from_segment_from_interpolation(z)

        self.distance, self.rho_z = z, rho_z
        self.length = self.distance[-1]
        self.itr_list = rho_z / self.rho_0
        self.adiabatic = self.get_adiabatic_factor(rho_z=self.rho_z, distance=self.distance)

        self.symmetric_distance = self.symmetrize_distance(z)
        self.symmetric_rho_z = self.symmetrize_array(self.rho_z)
        self.symmetric_itr_list = self.symmetrize_array(self.itr_list)
        self.symmetric_adiabatic = self.symmetrize_array(self.adiabatic)

    def get_adiabatic_factor(self, rho_z: numpy.ndarray, distance: numpy.ndarray) -> numpy.ndarray:
        r"""
        Compute the adiabatic factor defined as:
        .. math::
          f_c = \frac{1}{\rho} \frac{d \rho}{d z}

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """
        dz = numpy.gradient(distance, axis=0, edge_order=2)

        ditr = numpy.gradient(numpy.log(rho_z), axis=0, edge_order=2)

        return abs(ditr / dz)

    def _render_itr_vs_z_on_ax_(self, ax: Axis) -> None:
        """
        Add plot onto axis, the plots is ITR vs Z-distance
        
        :param      ax:   The axis on which to add the plot
        :type       ax:   Axis
        """
        ax.y_label = 'Inverse taper ratio'
        ax.x_label = 'z-distance'
        ax.y_scale = 'linear'

        artist = Line(
            x=self.symmetric_distance,
            y=self.symmetric_rho_z / self.rho_0
        )

        ax.add_artist(artist)

    def _render_adiabatic_vs_z_on_ax_(self, ax: Axis) -> None:    
        """
        Add plot onto axis, the plots is adiabatic criterion vs Z-distance
        
        :param      ax:   The axis on which to add the plot
        :type       ax:   Axis
        """
        ax.y_scale = 'log'        
        ax.y_label = 'Adiabatic criterion'
        ax.x_label = 'z-distance'

        artist = Line(
            x=self.symmetric_distance, 
            y=self.symmetric_adiabatic
        )

        ax.add_artist(artist)

    def _render_adiabatic_vs_itr_on_ax_(self, ax: Axis) -> None:    
        """
        Add plot onto axis, the plots is adiabatic criterion vs ITR
        
        :param      ax:   The axis on which to add the plot
        :type       ax:   Axis
        """
        ax.y_scale = 'log'        
        ax.y_label = 'Adiabatic criterion'
        ax.x_label = 'Inverse taper ratio (ITR)'

        artist = Line(
            x=self.itr_list, 
            y=self.adiabatic,
            line_style='--',
            color='k',
            label=self.name
        )

        ax.add_artist(artist)

    def plot(self) -> Scene2D:
        """
        Generate two plots: ITR vs z distance and adiabatic criterion vs ITR
        """

        itr = self.symmetric_rho_z / self.rho_0
        figure = Scene2D(title=f'Minimum ITR: {itr.min():.4f}')

        ax0 = Axis(row=0, col=0)

        ax1 = Axis(row=1, col=0)

        figure.add_axes(ax0, ax1)

        self._render_itr_vs_z_on_ax_(ax0)

        self._render_adiabatic_vs_itr_on_ax_(ax1)

        return figure

