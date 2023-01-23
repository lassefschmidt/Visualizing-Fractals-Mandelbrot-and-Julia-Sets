# import own .py files
import fractals.gufunc as gufunc

# import statements
import numpy as np
from scipy.interpolate import pchip_interpolate, Akima1DInterpolator, interp1d

class Fractal(object): 

    def __init__(self, width, height, max_iter, xlim, ylim, esc_radius_sq = 100.0):
        """
        Constructor method of Fractal class

        Args:
        -------
        width, height: int
            number of points we evaluate on x-, y-axis (directly influences rendering quality / resolution of image)
        max_iter: int
            maximum number of iterations to be computed for each point
        xlim, ylim: np.array containing 2 numeric values
            lower and upper limit on x- and y-axis
        esc_radius_sq: int
            squared escape radius (if |z|^2 = Z_real^2 + Z_i^2 becomes greater than the squared escape radius, we assume that it has escaped)
        """
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.xlim = xlim
        self.ylim = ylim
        self.esc_radius_sq= esc_radius_sq

    def get_grid(self):
        """Create coordinate grid based on xlim, ylim
        
        Returns
        -------
        the two outputs of np.meshgrid converted to pygame coordinates
        """
        # Build grid
        x, y = np.linspace(self.xlim[0], self.xlim[1], self.width), np.linspace(self.ylim[0], self.ylim[1], self.height)
        xx, yy = np.meshgrid(x, y)
        # return flipped xx, yy coordinates to plot fractal correctly in pygame (pygame starts with (0,0) in top right)
        return np.flip(xx, axis = 0), np.flip(yy, axis = 0)
        

    def get_coord(self, point):
        """transform pygame coordinates (point) to fractal coordinates on complex plane
        
        Args
        ----
        point: tuple of 2 integer (in pygame coordinates)

        Returns
        -------
        coordinates (numeric) of given point in complex plane of selected fractal instance
        """
        # decompose given tuple
        pg_x, pg_y = point[0], point[1]
        # get complex grid of fractal
        xx, yy = self.get_grid()
        # return transformed coordinates
        return xx[pg_y][pg_x], yy[pg_y][pg_x]

    def color_fractal(self, m, ms, cmap_id, unique_colors, interpolation_method, color_norm):
        """
        assign every point of fractal a color (RGB color space) 

        Sources:
        --------
        http://linas.org/art-gallery/escape/smooth.html
        http://linas.org/art-gallery/escape/escape.html
        https://rubenvannieuwpoort.nl/posts/smooth-iteration-count-for-the-mandelbrot-set
        https://csl.name/post/mandelbrot-rendering/
        
        Args
        ----
        m: np.array
            array of simple iteration count of fractal
        ms: np.array
            array of smoothed iteration count of fractal
        cmap_id: integer
            id of desired colormap
        unique_colors: integer
            desired amount of unique colors in colormap
        interpolation_method: integer
            id of desired interpolation method
        color_norm: integer
            id of desired normalization method to choose whether we color the fractal based on m (simple iteration count) or ms (smoothed iteration count)
        
        Returns
        -------
        mu_rgb: np.array
            contains RGB color for every single point we evaluated on the complex plane
        """
        # create color map
        x_obs, y_obs, color_max = self.get_cmap(cmap_id)
        cmap, fact_upperbound = self.interpolate_cmap(unique_colors, interpolation_method, x_obs, y_obs)

        if color_norm == 0: # choose color with simple iteration count
            mu = np.mod(m, len(cmap))
        elif color_norm == 1: # choose color with smoothed iteration count
            mu = (ms * fact_upperbound).astype(int) % len(cmap)

        # replace every element in mu with the rgb values from our cmap
        mu_rgb = self.fetch_iter_color(mu, cmap)
        mu_rgb[m == self.max_iter] = color_max

        return mu_rgb

    def get_cmap(self, cmap_id):
        """
        Fetch control points of chosen color map in RGB color space

        Args
        ----
        cmap_id: integer
            id of desired colormap

        Returns
        -------
        x_obs: list[int]
            contains x-values of control points of chosen color map
        y_obs: list[list[int]]
            contains RGB-values of control points of chosen color map
        color_max: list[int]
            contains RBG-values for points that never escape
        """
        if cmap_id == 0:
            x_obs = [0, .16, .42, .64, .86, 1]
            yR_obs= [0, 32, 237, 255, 0, 0]
            yG_obs = [7, 107, 255, 170, 2, 7]
            yB_obs = [100, 203, 255, 0, 0, 100]
            ##---------Reference taken from---------#
            # https://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
        elif cmap_id == 1:
            x_obs = [0, .16, .32, .48, .64, .80, .96]
            yR_obs= [253, 254, 195, 82, 36, 113, 17]
            yG_obs = [252, 217, 130, 16, 17, 184, 3]
            yB_obs = [223, 88, 23, 30, 80, 250, 64]
            ##---------Reference taken from---------#
            # https://courses.lumenlearning.com/math4liberalarts/chapter/introduction-exponential-and-logistic-growth/
        elif cmap_id == 2:
            x_obs = [0, .142, .284, .426, .568, .71, .852, 1]
            yR_obs= [129, 202, 0, 254, 154, 1, 0, 0]
            yG_obs = [25, 53, 243, 144, 230, 66, 146, 2]
            yB_obs = [31, 199, 86, 215, 209, 255, 61, 0]
            ##---------Reference taken from---------#
            # https://parametrichouse.com/the-mandelbrot-set/
        elif cmap_id == 3:
            x_obs = [0, 1]
            yR_obs= [210, 4]
            yG_obs = [224, 4]
            yB_obs = [151, 7]
            #---------Reference taken from---------#
            # https://www.shutterstock.com/image-illustration/fractal-artwork-part-called-mandelbrot-set-1464500327
        elif cmap_id == 4:
            # set control points
            x_obs = [0, .25, .50, .75, 1]
            yR_obs= [6, 6, 7, 119, 218]
            yG_obs = [12, 95, 152, 211, 234]
            yB_obs = [15, 104, 138, 149, 155]
            #---------Reference taken from---------#
            # https://www.shutterstock.com/image-illustration/fractal-artwork-part-called-mandelbrot-set-1464500327

        color_max = [0, 0, 0] # set desired color for values that never escape

        return x_obs, [yR_obs, yG_obs, yB_obs], color_max

    def interpolate_cmap(self, unique_colors, interpolation_method, x_obs, y_obs, fact_lowerbound = 0, fact_upperbound = 255):
        """
        take control points of chosen color map and create full cmap based on chosen interpolation_method (with as many colors as unique_colors)

        Sources
        -------
        https://blogs.mathworks.com/cleve/2019/04/29/makima-piecewise-cubic-interpolation/

        Args
        ----
        unique_colors: integer
            desired amount of unique colors in colormap
        interpolation_method: integer
            id of desired interpolation method
        x_obs: list[int]
            contains x-values of control points of chosen color map
        y_obs: list[list[int]]
            contains RGB-values of control points of chosen color map
        fact_lowerbound, fact_upperbound: integer
            lower- and upperbound of chosen colorspace (RGB starts with 0 and ends with 255)

        Returns
        -------
        cmap: nd.array
            colormap in nd.array with shape (unique_colors, 3), in which every row contains a specific RGB color
        fact_upperbound: integer
            upperbound of chosen colorspace
        """
        # create interpolated x-axis
        x = np.linspace(min(x_obs), max(x_obs), unique_colors)
        # choose interpolation method
        if interpolation_method == 0: # linear interpolation 
            for i, y in enumerate(y_obs):
                f_i = interp1d(x_obs, y, kind = 'linear')
                y_obs[i] = f_i(x).astype(np.int64)
        elif interpolation_method == 1: # monotone cubic interpolation with more curves
            for i, y in enumerate(y_obs):
                f_i = Akima1DInterpolator(x_obs, y)
                y_obs[i] = f_i(x).astype(np.int64)
        elif interpolation_method == 2: # monotone cubic interpolation with fewer curves
            for i, y in enumerate(y_obs):
                y_obs[i] = pchip_interpolate(x_obs, y, x).astype(np.int64)
        # swap rows and columns so that each row denotes a color
        cmap = np.transpose(y_obs, (1,0))
        # remove potential out of range values and replace them with the bounds of our factor
        cmap[cmap < fact_lowerbound] = fact_lowerbound
        cmap[cmap > fact_upperbound] = fact_upperbound
        
        return cmap, fact_upperbound

    def fetch_iter_color(self, mu, cmap):
        """Fetch every color based on mu (the value of every element in mu is the color_id, which corresponds to a specific row in the color map)
        
        Args
        ----
        mu: nd.array
            normalized array of simple / smoothed iteration count of fractal (normalized with mod n, where n equals number of rows in chosen colormap)
        cmap: nd.array
            colormap in nd.array with shape (unique_colors, 3), in which every row contains a specific RGB color
        
        Returns
        -------
        mu_rgb: np.array
            contains RGB color for every single point we evaluated on the complex plane (values that never escape are not correctly colored yet)
        """
        mu_rgb = gufunc.fetch_iter_color_numpy_gu(mu, cmap)
        return mu_rgb

    def zoom(self, point, zoom_factor):
        """zooms / moves towards given point (in complex coordinates) in Fractal (updates xlim, ylim instance variables)
        
        Args
        ----
        point: tuple of 2 integer (in complex coordinates of given fractal)
        zoom_factor: float
            if equal to 1, we center the image at the given point without zooming in or out; if greater 1, we zoom in; if smaller 1, we zoom out
        """
        # decompose complex coordinates of selected point
        c_x, c_y = point[0], point[1]
        # calculate new limits
        width, height = self.xlim[1] - self.xlim[0], self.ylim[1] - self.ylim[0]
        new_width, new_height = (1 / zoom_factor) * width, (1 / zoom_factor) * height
        new_xlim, new_ylim = np.array([c_x - new_width * 0.5, c_x + new_width * 0.5]), np.array([c_y - new_height * 0.5, c_y + new_height * 0.5])
        # assign new limits to instance
        self.xlim, self.ylim = new_xlim, new_ylim

class Mandelbrot(Fractal):

    def __init__(self, width, height, max_iter, esc_radius_sq = 100.0, xlim = np.array([-2.5, 1.5]), ylim = np.array([-2, 2])):
        super().__init__(width, height, max_iter, esc_radius_sq = esc_radius_sq, xlim = xlim, ylim = ylim)

    def calc(self):
        """
        generates mandelbrot set

        Returns
        -------
        m: np.array
            number of iterations when point x_{i}, y_{j} escaped or reached max_iter (simple iteration count)
        ms: np.array
            fractionalised number of iterations when point x_{i}, y_{j} escaped or reached max_iter (smoothed iteration count)
        """
        # set up grid
        xx, yy = self.get_grid()
        # create complex plane Z
        Z = xx + yy*1j
        # calculate iterations (in each iteration, square every point on complex plane C and add it again)
        m, ms = gufunc.mandelbrot_numpy_gu(Z, self.max_iter, self.esc_radius_sq)

        return m, ms

class JuliaSet(Fractal):

    def __init__(self, width, height, max_iter, C = 0 + 0*1j, esc_radius_sq= 10.0, xlim = np.array([-2, 2]), ylim = np.array([-2, 2])):
        super().__init__(width, height, max_iter, esc_radius_sq = esc_radius_sq , xlim=xlim, ylim=ylim)
        self.C = C # constant point C for which we want to calculate the Julia set

    def calc(self):
        """
        generates Julia set

        Returns
        -------
        m: np.array
            number of iterations when point x_{i}, y_{j} escaped or reached max_iter (simple iteration count)
        ms: np.array
            fractionalised number of iterations when point x_{i}, y_{j} escaped or reached max_iter (smoothed iteration count)
        """
        # set up grid
        xx, yy = self.get_grid()
        # create complex plane Z 
        Z = xx + yy * 1j
        # calculate iterations (in each iteration, add add chosen C (complex constant) to the square of every single point on complex plane Z)
        m, ms = gufunc.julia_numpy_gu(Z, self.C, self.max_iter, self.esc_radius_sq)

        return m, ms