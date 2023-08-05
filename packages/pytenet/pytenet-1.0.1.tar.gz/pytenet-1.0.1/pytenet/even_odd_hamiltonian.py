import numpy as np


def heisenberg_XXZ_twosite(L, J, h):
    """
    Construct XXZ Heisenberg Hamiltonian
    'sum J[0] X X + J[1] Y Y + J[2] Z Z - h Z' on a 1D lattice
    based on local two-site operators.
    """

    assert L >= 2, 'need at least two lattice sites'

    XX = 0.25 * np.array(
        [[ 0,  0,  0,  1 ],
         [ 0,  0,  1,  0 ],
         [ 0,  1,  0,  0 ],
         [ 1,  0,  0,  0 ]], dtype=float)
    YY = 0.25 * np.array(
        [[ 0,  0,  0, -1 ],
         [ 0,  0,  1,  0 ],
         [ 0,  1,  0,  0 ],
         [-1,  0,  0,  0 ]], dtype=float)
    ZZ = 0.25 * np.array(
        [[ 1,  0,  0,  0 ],
         [ 0, -1,  0,  0 ],
         [ 0,  0, -1,  0 ],
         [ 0,  0,  0,  1 ]], dtype=float)

    Sid = 0.5 * np.array(
        [[ 1,  0,  0,  0 ],
         [ 0,  1,  0,  0 ],
         [ 0,  0, -1,  0 ],
         [ 0,  0,  0, -1 ]], dtype=float)
    idS = 0.5 * np.array(
        [[ 1,  0,  0,  0 ],
         [ 0, -1,  0,  0 ],
         [ 0,  0,  1,  0 ],
         [ 0,  0,  0, -1 ]], dtype=float)

    # local two-site terms
    T = J[0]*XX + J[1]*YY + J[2]*ZZ

    h2 = []
    for j in range(L - 1):
        h2.append(T - h*((1.0 if j == 0     else 0.5)*Sid +
                         (1.0 if j == L - 2 else 0.5)*idS))

    return h2
