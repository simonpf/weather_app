"""
The weather_app.render module
=============================

The :code:`wether_app.render` module provides functionality to render weather
forecast data as ASCII plots. All functionality is implemented by the
AsciiGraph class.

"""
import numpy as np

_RED = '\033[31m'
_BLUE = '\033[34m'
_END_COLOR = '\033[0m'

class AsciiGraph:
    """
    Drawing graphs as ASCII string.

    The AsciiGraph class represents a graph to be rendered to a string
    using ASCII characters.

    Attributes:
        height(int): The height of the plot in lines.
        color(Boolean): Whether or not to use BASH color codes in output.
        grid(np.array): Numpy array containing the characters for each
             position in the panel.
        I_ZERO: Grid index corresponding to 0 on the y-axis.
        I_MAX: Grid index corresponding the maximum y-value.
        J_ZERO: Grid index corresponding to 0 on the x-axis.
        J_MAX: Grid index corresponding the maximum x-value.
    """
    def __draw_axes__(self):

        # Left y-axis
        self.grid[self.I_MAX:self.I_ZERO, self.J_ZERO] = "|"
        self.grid[self.I_MAX, self.J_ZERO] = "^"

        # x-axis
        self.grid[self.I_ZERO, self.J_ZERO:self.J_MAX] = "-"
        self.grid[self.I_ZERO, self.J_MAX] = ">"

        # Coordinate cross
        self.grid[self.I_ZERO, self.J_ZERO] = "+"

        center = 79 // 2
        self.__write__(self.height + 2, center - 2, "Time")


        one_third = 79 // 3
        s = " : Temperature"
        start = one_third - (len(s) + 1) // 2
        self.grid[0, start] = self.temperature_marker
        self.__write__(0, start + 1, s)


        two_thirds = 79 // 3 * 2
        s = " : Precipitation"
        start = two_thirds - (len(s) + 1) // 2
        self.grid[0, start] = self.precipitation_marker
        self.__write__(0, start + 1, s)

        self.t_limits = None
        self.p_limits = None


    def __write__(self, i, j, what):
        for k, c in enumerate(what):
            self.grid[i, j + k] = c

    def __init__(self, height = 40, color=True):
        """
        Args:
            height(int): The vertical of the plotting area of the graph in lines.
            color(Bool): Whether or not to use BASH color codes when rendering
            the graph.
        """
        self.height = height
        self.I_ZERO = self.height + 3 -4
        self.I_MAX =  2
        self.J_ZERO = 4
        self.J_MAX = 72
        self.grid = np.array([[" "] * 79] * (self.height + 4), dtype='object')
        # Color codes
        self.color = color
        self.__draw_axes__()

    def add_temperature_plot(self, x, y):
        """
        Add temperature plot to the graph.

        Draws the given temperature sequence into the plot.

        Args:
            x(array): 1D array containing the x coordinates of the sequence.
            y(array): 1D array containing the corresponding temperatures.
        """
        x = np.array(x)
        y = np.array(y)
        t_min = y.min()
        t_max = y.max()
        self.t_limits = (t_min, t_max)
        n = self.J_MAX - self.J_ZERO
        m = self.I_ZERO - self.I_MAX
        dt = (t_max - t_min) / m

        x_graph = np.linspace(x[0], x[-1], n)
        y_graph = np.interp(x_graph, x, y)
        i_indices = np.round((y_graph - t_min) / dt)
        for j, i in enumerate(i_indices):
            i = int(i)
            if (i > 0) and (j > 0) and (j < n):
                self.grid[self.I_ZERO - i, self.J_ZERO + j] = self.temperature_marker


    def add_precipitation_plot(self, x, y):
        """
        Add precipitation plot to the graph.

        Draws the given precipitation sequence into the plot.

        Args:
            x(array): 1D array containing the x coordinates of the sequence.
            y(array): 1D array containing the corresponding precipitation.
        """
        x = np.array(x)
        y = np.array(y)
        p_min = 0.0
        p_max = 5.0
        self.p_limits = (p_min, p_max)
        n = self.J_MAX - self.J_ZERO
        m = self.I_ZERO - self.I_MAX
        dt = (p_max - p_min) / m

        x_graph = np.linspace(x[0], x[-1], n)
        y_graph = np.interp(x_graph, x, y)
        i_indices = np.floor((y_graph - p_min) / dt)
        for j, i in enumerate(i_indices):
            i = int(i)
            if (i > 0) and (j > 0) and (j < n):
                self.grid[self.I_ZERO - i : self.I_ZERO, self.J_ZERO + j] = self.precipitation_marker

    def set_time_range(self, t0, t1):
        """
        Set the x-axis range of the plot.

        This draws x-labels onto the plot according the given start and end times
        of the plotted sequences.

        Args:
            t0(datetime): The time to associate with the leftmost column of
                the plot.
            t1(datetime): The time to associate with the rightmost column of
                the plot.
        """
        n = self.J_MAX - self.J_ZERO
        dt = (t1 - t0) / n
        for j in range(2, n, 10):
            t = t0 + dt * j
            s = t.strftime("%H:%M")
            self.__write__(self.I_ZERO + 1, self.J_ZERO + j - 2, s)

    @property
    def temperature_marker(self):
        """The marker (including color codes) used to draw temperatures."""
        if (self.color):
            return _RED + '.' + _END_COLOR
        else:
            return "."

    @property
    def precipitation_marker(self):
        """The marker (including color codes) used to draw precipitation."""
        if (self.color):
            return _BLUE + 'x' + _END_COLOR
        else:
            return "x"


    def render(self):
        """
        Prints the resulting graph to the standard out.
        """
        print("\n")

        if self.t_limits:
            t_min, t_max = self.t_limits
            self.__write__(0, 2, "T [C]")
            for i in range(0, self.height, 5):
                dy = i / self.height
                y = t_min + dy * (t_max - t_min)
                s = f"{y:3.0f}"
                self.__write__(self.I_ZERO - i, 0, s)

        if self.p_limits:
            p_min, p_max = self.p_limits
            self.__write__(0, self.J_MAX - 1, "P [mm/h]")
            for i in range(0, self.height, 5):
                dy = i / self.height
                y = p_min + dy * (p_max - p_min)
                s = f"{y:4.1f}"
                self.__write__(self.I_ZERO - i, self.J_MAX + 1, s)

        for l in self.grid:
            print("".join(l))
