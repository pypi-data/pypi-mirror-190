import numpy as np
import warnings
#from .qnumber import qnumber_outer_sum, qnumber_flatten, is_qsparse
#from .bond_ops import qr, split_matrix_svd

__all__ = ['iMPS', 'left_orthonormalize']


class iMPS(object):
    """
    Uniform ("infinite") matrix product state (MPS) class.
    """

    def __init__(self, qd, qD, fill=0.0):
        """
        Create a matrix product state.

        Args:
            qd: physical quantum numbers at each site
        """
        # require NumPy arrays
        self.qd = np.array(qd)
        self.qD = np.array(qD)
        d = len(qd)
        D = len(qD)
        self.A = np.full((d, D, D), fill)

        ## create list of MPS tensors
        #D = [len(qb) for qb in qD]
        ## leading and trailing bond dimensions must be 1
        #assert D[0] == 1 and D[-1] == 1
        #if isinstance(fill, int) or isinstance(fill, float) or isinstance(fill, complex):
        #    self.A = [np.full((d, D[i], D[i+1]), fill) for i in range(len(D)-1)]
        #elif fill == 'random':
        #    # random complex entries
        #    self.A = [
        #            np.random.normal(size=(d, D[i], D[i+1]), scale=1./np.sqrt(d*D[i]*D[i+1])) +
        #         1j*np.random.normal(size=(d, D[i], D[i+1]), scale=1./np.sqrt(d*D[i]*D[i+1])) for i in range(len(D)-1)]
        #else:
        #    raise ValueError('fill = {} invalid; must be a number or "random".'.format(fill))
        ## enforce block sparsity structure dictated by quantum numbers
        #for i in range(len(self.A)):
        #    mask = qnumber_outer_sum([self.qd, self.qD[i], -self.qD[i+1]])
        #    self.A[i] = np.where(mask == 0, self.A[i], 0)


def left_orthonormalize(A, L, eta):
    """
    Left-orthonormalize a uniform MPS tensor.

    Args:
        A: input MPS tensor, of shape (d, D, D)
        L: initial guess for L matrix, of shape (D, D)
        eta: convergence tolerance

    Returns:
        tuple: tuple containing
          - A: left-orthogonal A tensor
          - L: corresponding L matrix

    Reference:
        L. Vanderstraeten, J. Haegeman, F. Verstraete
        Tangent-space methods for uniform matrix product states
        arXiv:1810.07006
    """
    assert A.ndim == 3

    s = A.shape
    assert s[1] == s[2], 'left and right virtual bond dimensions must agree'

    L = L / np.linalg.norm(L)
    nL = 1

    i = 0
    maxiter = 2000

    delta = eta + 1
    while delta > eta:
        # iteratively update L
        LA = np.tensordot(L, A, axes=(1, 1)).transpose((1, 0, 2))
        ###print('LA.shape:', LA.shape)
        Aleft, Lnext = np.linalg.qr(LA.reshape((-1, LA.shape[2])), mode='reduced')
        Aleft = Aleft.reshape(s)
        nL = np.linalg.norm(Lnext)
        Lnext /= nL
        delta = np.linalg.norm(Lnext - L)
        ##print('delta:', delta)
        L = Lnext
        i += 1
        if i > maxiter:
            warnings.warn(
                'Maximum number of iterations ({}) reached during left '
                'orthonormalization, current delta: {:g}.'.format(maxiter, delta),
                RuntimeWarning)
            break

    return Aleft, L, nL
