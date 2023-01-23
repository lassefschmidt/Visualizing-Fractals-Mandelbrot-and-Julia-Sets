# import statements
import math
import numba
from numba import jit, guvectorize, float64, int64, complex128

# functions to calculate mandelbrot set
@jit(numba.typeof((42, 0.))(complex128, int64, float64))
def mandelbrot_gu(z, max_iter, esc_radius_sq):
    """compute all mandelbrot iterations for a given point on the complex plane of the fractal
    
    Args
    ----
    z: complex128
        current point on complex plane for which we evaluate its simple & smoothed iteration count
    max_iter: int
        maximum number of iterations to be computed for each point
    esc_radius_sq: int
        squared escape radius (if |z|^2 = Z_real^2 + Z_i^2 becomes greater than the squared escape radius, we assume that it has escaped)

    Returns
    -------
    tuple containing the simple and smoothed iteration count for the given point z
    """
    mreal = 0
    real = 0
    imag = 0
    for m in range(max_iter):
        mreal = real*real - imag*imag + z.real
        imag = 2* real*imag + z.imag
        real = mreal
        if real * real + imag * imag > esc_radius_sq: # if value escapes before reaching max_iter
            return (m, m + 2 - math.log(math.log(real * real + imag * imag))/math.log(2))
        if m == max_iter - 1: # if value does not escape before reaching max_iter
            return (max_iter, 0)
    return (0, 0)

@guvectorize([(complex128[:], int64[:], float64[:], int64[:], float64[:])], '(n),(),()->(n),(n)',target='parallel')
def mandelbrot_numpy_gu(Z, max_iter, esc_radius_sq, m_output, ms_output):
    """Vectorizes the mandelbrot calculation and runs it multithreaded
    
    Args
    ----
    Z: np.array
        array that contains all complex values we want to evaluate on the complex plane of the mandelbrot fractal
    max_iter: int
        maximum number of iterations to be computed for each point
    esc_radius_sq: int
        squared escape radius (if |z|^2 = Z_real^2 + Z_i^2 becomes greater than the squared escape radius, we assume that it has escaped)

    Returns
    -------
    m_output: np.array
        number of iterations when point x_{i}, y_{j} escaped or reached max_iter (simple iteration count)
    ms_output: np.array
        fractionalised number of iterations when point x_{i}, y_{j} escaped or reached max_iter (smoothed iteration count)
    """
    max_iter = max_iter[0]
    esc_radius_sq = esc_radius_sq[0]
    for i in range(Z.shape[0]):
        m_output[i], ms_output[i] = mandelbrot_gu(Z[i],max_iter, esc_radius_sq)

# functions to calculate julia set
@jit(numba.typeof((42, 0.))(complex128, complex128, int64, float64))
def julia_gu(z, c, max_iter, esc_radius_sq):
    """compute all julia iterations for a given point on the complex plane of the fractal
    
    Args
    ----
    z: complex128
        current point on complex plane for which we evaluate its simple & smoothed iteration count
    c: complex 128
        chosen constant complex value with which we will evaluate z
    max_iter: int
        maximum number of iterations to be computed for each point
    esc_radius_sq: int
        squared escape radius (if |z|^2 = Z_real^2 + Z_i^2 becomes greater than the squared escape radius, we assume that it has escaped)

    Returns
    -------
    tuple containing the simple and smoothed iteration count for the given point z
    """
    mreal = 0
    real = z.real
    imag = z.imag
    for m in range(max_iter):
        mreal = real*real - imag*imag + c.real
        imag = 2* real*imag + c.imag
        real = mreal
        if real * real + imag * imag > esc_radius_sq: # if value escapes before reaching max_iter
            return (m + 1, m + 3 - math.log(math.log(real * real + imag * imag))/math.log(2))
        if m == max_iter - 1: # if value does not escape before reaching max_iter
            return (max_iter, 0)
    return (0, 0)

@guvectorize([(complex128[:], complex128[:], int64[:], float64[:], int64[:], float64[:])], '(n),(),(),()->(n),(n)',target='parallel')
def julia_numpy_gu(Z, C, max_iter, esc_radius_sq, m_output, ms_output):
    """Vectorizes the Julia set calculation and runs it multithreaded
    
    Args
    ----
    Z: np.array
        array that contains all complex values we want to evaluate on the complex plane of the Julia set
    C: complex128
        constant complex value that we will add in each iteration to every point on complex plane to calculate Julia set
    max_iter: int
        maximum number of iterations to be computed for each point
    esc_radius_sq: int
        squared escape radius (if |z|^2 = Z_real^2 + Z_i^2 becomes greater than the squared escape radius, we assume that it has escaped)

    Returns
    -------
    m_output: np.array
        number of iterations when point x_{i}, y_{j} escaped or reached max_iter (simple iteration count)
    ms_output: np.array
        fractionalised number of iterations when point x_{i}, y_{j} escaped or reached max_iter (smoothed iteration count)
    """
    max_iter = max_iter[0]
    esc_radius_sq = esc_radius_sq[0]
    C = C[0]
    for i in range(Z.shape[0]):
        m_output[i], ms_output[i] = julia_gu(Z[i], C, max_iter, esc_radius_sq)

# function to color fractal
@guvectorize([(int64[:,:], int64[:,:], float64[:,:,:])], '(m,n),(i,j)->(m,n,j)',target='parallel')
def fetch_iter_color_numpy_gu(mu, cmap, output):
    """generate new array of shape (m,n,3) that contains the RGB values for all single iteration counts in mu
    
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
    for i in range(mu.shape[0]): # iterate through rows in mu
        for j in range(mu.shape[1]): # iterate through columns in mu
            cur_mu = mu[i][j]
            output[i][j] = cmap[cur_mu]