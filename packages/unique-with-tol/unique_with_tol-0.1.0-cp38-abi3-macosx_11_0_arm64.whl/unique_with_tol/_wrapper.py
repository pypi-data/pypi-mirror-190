import numpy as np
from .unique_with_tol import indices_unique_with_tol


def unique_with_tol(
    a: np.array,
    tol: float,
    *,
    return_inverse: bool = False,
    return_counts: bool = False,
    axis: int = 0
):
    """Find unique elements of an array with a tolerance.

    It is equivalent to creating a graph in which two nodes are connected if
    their distance is less than the tolerance. Then, the connected components
    of the graph are the unique elements. If the connected components are not
    cliques (fully connected), the function raises an error.

    Parameters
    ----------
    a : array_like
        Input array
    tol : float
        Tolerance
    return_inverse : bool, optional
        If True, also return the indices of the cluster for each input element.
    return_counts : bool, optional
        If True, also return the number of elements in each cluster.
    axis : int, optional
        Axis along which to find unique elements. Default is 0.

    Returns
    -------
    unique : ndarray
        The center of each cluster.
    """
    assert a.ndim >= 1
    a = np.moveaxis(a, axis, 0)

    a_flat = a.reshape(a.shape[0], -1)
    inverses = indices_unique_with_tol(a_flat, tol)

    counts = np.bincount(inverses)

    centers = np.zeros((np.max(inverses) + 1, a_flat.shape[1]))
    np.add.at(centers, inverses, a_flat)
    centers /= counts[:, None]

    centers = centers.reshape((centers.shape[0],) + a.shape[1:])
    centers = np.moveaxis(centers, 0, axis)

    returns = (centers,)
    if return_inverse:
        returns = returns + (inverses,)
    if return_counts:
        returns = returns + (counts,)

    return returns if len(returns) > 1 else returns[0]
