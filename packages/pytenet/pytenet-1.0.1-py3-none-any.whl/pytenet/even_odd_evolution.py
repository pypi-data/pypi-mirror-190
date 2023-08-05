import numpy as np
from scipy.linalg import expm
from mps import merge_MPS_tensor_pair, split_MPS_tensor


def integrate_even_odd_strang(h2, psi, dt, numsteps, tol):
    """Time evolution using Strang splitting applied to even-odd bonds."""

    # number of lattice sites
    L = psi.nsites
    assert L == len(h2) + 1

    exp_h2 = [expm(-0.5 * dt * op) for op in h2]

    for n in range(numsteps):

        # sweep from left to right
        for i in range(L - 1):
            A = merge_MPS_tensor_pair(psi.A[i], psi.A[i+1])
            # apply local two-site operator
            A = np.tensordot(exp_h2[i], A, axes=1)
            (psi.A[i], psi.A[i+1]) = split_MPS_tensor(A, psi.d, psi.d, 'right', tol)

        # sweep from right to left
        for i in reversed(range(L - 1)):
            A = merge_MPS_tensor_pair(psi.A[i], psi.A[i+1])
            # apply local two-site operator
            A = np.tensordot(exp_h2[i], A, axes=1)
            (psi.A[i], psi.A[i+1]) = split_MPS_tensor(A, psi.d, psi.d, 'left', tol)
