import numpy as np


def contraction_operator_step_right2(A, B, W, R):
    """
    Contraction step from right to left, with a matrix product operator
    sandwiched in between.

    To-be contracted tensor network::

          _____           ______
         /     \         /
      ---|1 B*2|---   ---|2
         \__0__/         |
            |            |
                         |
          __|__          |
         /  0  \         |
      ---|2 W 3|---   ---|1   R
         \__1__/         |
            |            |
                         |
          __|__          |
         /  0  \         |
      ---|1 A 2|---   ---|0
         \_____/         \______
    """

    assert A.ndim == 3
    assert B.ndim == 3
    assert W.ndim == 4
    assert R.ndim == 3

    # multiply with A tensor
    T = np.tensordot(A, R, 1)

    # multiply with W tensor
    T = np.tensordot(W, T, axes=((1, 3), (0, 2)))

    # interchange levels 0 <-> 2 in T
    T = T.transpose((2, 1, 0, 3))

    # multiply with conjugated B tensor
    Rnext = np.tensordot(T, B.conj(), axes=((2, 3), (0, 2)))

    return Rnext


def operator_inner_product(chi, op, psi):
    """
    Compute the inner product `<chi | op | psi>`.

    Args:
        chi: wavefunction represented as MPS
        op:  operator represented as MPO
        psi: wavefunction represented as MPS

    Returns:
        complex: `<chi | op | psi>`
    """

    assert psi.nsites == chi.nsites
    assert psi.nsites == op.nsites

    if psi.nsites == 0:
        return 0

    # initialize T by identity tensor
    T = np.array([[[1]]], dtype=psi.A[-1].dtype)

    for i in reversed(range(psi.nsites)):
        T = contraction_operator_step_right2(psi.A[i], chi.A[i], op.A[i], T)

    # T should now be a 1x1x1 tensor
    assert T.shape == (1, 1, 1)

    return T[0, 0, 0]


def compute_local_hamiltonian(L, R, W):
    """
    Compute site-local Hamiltonian operator (for test purposes).

    To-be contracted tensor network::
     ______                           ______
           \                         /
          2|---                   ---|2
           |                         |
           |                         |
           |                         |
           |          __|__          |
           |         /  0  \         |
      L   1|---   ---|2 W 3|---   ---|1   R
           |         \__1__/         |
           |            |            |
           |                         |
           |                         |
           |                         |
          0|---                   ---|0
     ______/                         \______


    Indexing for np.einsum:
     ______                           ______
           \                         /
          2|---                   ---|5
           |                         |
           |                         |
           |                         |
           |          __|__          |
           |         /  6  \         |
      L   1|---   ---|1 W 4|---   ---|4   R
           |         \__7__/         |
           |            |            |
           |                         |
           |                         |
           |                         |
          0|---                   ---|3
     ______/                         \______

    """
    assert L.ndim == 3
    assert R.ndim == 3
    assert W.ndim == 4

    return np.einsum(L, (0, 1, 2), R, (3, 4, 5), W, (6, 7, 1, 4), (6, 2, 5, 7, 0, 3))


def compute_local_bond_contraction(L, R):
    """
    Compute "zero-site" bond contraction operator.

    To-be contracted tensor network::
     ______                           ______
           \                         /
          2|---                   ---|2
           |                         |
           |                         |
           |                         |
           |                         |
           |                         |
      L   1|-----------   -----------|1   R
           |                         |
           |                         |
           |                         |
           |                         |
           |                         |
          0|---                   ---|0
     ______/                         \______
    """

    assert L.ndim == 3
    assert R.ndim == 3

    # multiply L with R tensor and interchange dimensions
    return np.tensordot(L, R, axes=(1, 1)).transpose((1, 3, 0, 2))
