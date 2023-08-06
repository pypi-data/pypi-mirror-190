import numpy as np
from unique_with_tol import unique_with_tol


def test_1d():
    a, i, c = unique_with_tol(
        np.array([1.0, 1.1, 0.9, 4.0, 4.4, 1.0]),
        1.0,
        return_inverse=True,
        return_counts=True,
    )

    np.testing.assert_allclose(a, np.array([1.0, 4.2]))
    np.testing.assert_equal(i, np.array([0, 0, 0, 1, 1, 0]))
    np.testing.assert_equal(c, np.array([4, 2]))


def test_2d():
    a, i, c = unique_with_tol(
        np.array(
            [
                [1.0, 1.1],
                [0.9, 4.0],
                [4.4, 0.9],
                [1.0, 1.1],
                [4.1, 1.2],
                [4.4, 1.2],
            ]
        ),
        0.5,
        return_inverse=True,
        return_counts=True,
    )

    np.testing.assert_allclose(
        a,
        np.array(
            [
                [1.0, 1.1],
                [0.9, 4.0],
                [4.3, 1.1],
            ]
        ),
    )
    np.testing.assert_equal(i, np.array([0, 1, 2, 0, 2, 2]))
    np.testing.assert_equal(c, np.array([2, 1, 3]))
