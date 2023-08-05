import numpy as np
import copy
from typing import Sequence
from .qnumber import qnumber_outer_sum, qnumber_flatten, is_qsparse
from .bond_ops import qr

__all__ = ['MPO', 'merge_MPO_tensor_pair']


class MPO(object):
    """
    Matrix product operator (MPO) class.

    The i-th MPO tensor has dimension `[d, d, D[i], D[i+1]]` with `d` the physical
    dimension at each site and `D` the list of virtual bond dimensions.

    Quantum numbers are assumed to be additive and stored as integers.
    `qd` stores the list of physical quantum numbers at each site (assumed to agree
    for first and second physical dimension), and `qD` the virtual bond quantum numbers.
    The sum of first physical and left virtual bond quantum number of each
    non-zero tensor entry must be equal to the sum of second physical and
    right virtual bond quantum number.
    """

    def __init__(self, qd: Sequence[int], qD: Sequence[Sequence[int]], fill=0.0):
        """
        Create a matrix product operator.

        Args:
            qd: physical quantum numbers at each site (same for all sites)
            qD: virtual bond quantum numbers (list of quantum number lists)
            fill: explicit scalar number to fill MPO tensors with, or
                  'random' to initialize tensors with random complex entries
        """
        # require NumPy arrays
        self.qd = np.array(qd)
        self.qD = [np.array(qDi) for qDi in qD]
        # create list of MPS tensors
        d = len(qd)
        D = [len(qDi) for qDi in qD]
        if isinstance(fill, int) or isinstance(fill, float) or isinstance(fill, complex):
            self.A = [np.full((d, d, D[i], D[i+1]), fill) for i in range(len(D)-1)]
        elif fill == 'random':
            # random complex entries
            self.A = [
                    np.random.normal(size=(d, d, D[i], D[i+1]), scale=1./np.sqrt(d*D[i]*D[i+1])) +
                 1j*np.random.normal(size=(d, d, D[i], D[i+1]), scale=1./np.sqrt(d*D[i]*D[i+1])) for i in range(len(D)-1)]
        else:
            raise ValueError(f'fill = {fill} invalid; must be a number or "random".')
        # enforce block sparsity structure dictated by quantum numbers
        for i in range(len(self.A)):
            mask = qnumber_outer_sum([self.qd, -self.qd, self.qD[i], -self.qD[i+1]])
            self.A[i] = np.where(mask == 0, self.A[i], 0)

    @classmethod
    def identity(cls, qd: Sequence[int], L: int, scale: float = 1, dtype=complex):
        """
        Construct MPO representation of the identity operation.
        """
        d = len(qd)
        mpo = cls(qd, (L+1)*[[0]])
        for i in range(L):
            mpo.A[i] = scale * np.identity(d, dtype=dtype).reshape((d, d, 1, 1))
        return mpo

    @classmethod
    def from_opchains(cls, qd: Sequence[int], L: int, opchains):
        """
        Construct a MPO representation of a sum of "operator chains".

        Args:
            qd: physical quantum numbers at each site (same for all sites)
            L:  number of lattice sites
            opchains: list of operator chains

        Returns:
            MPO: MPO representation of `opchains`
        """

        # filter out empty operator chains
        opchains = [opc for opc in opchains if opc.length > 0]

        if len(opchains) == 0:
            # dummy zero tensors
            return cls(qd, (L+1)*[[0]], fill=0j)

        d = len(qd)

        opchains = sorted(opchains, key=lambda o: o.iend*L + o.length)

        # right-pad first operator chain with identity matrices
        # (required for trailing identity operations in each chain)
        opchains[0] = copy.deepcopy(opchains[0])
        opchains[0].pad_identities_right(d, L)

        # find operator chain with largest starting index
        maxidxS = np.argmax([op.istart for op in opchains])
        # left-pad this operator chain with identity matrices (for leading identity operations in each chain)
        opchains[maxidxS] = copy.deepcopy(opchains[maxidxS])
        opchains[maxidxS].pad_identities_left(d)

        # allocate virtual bond slots between operators for each operator chain
        slotidx = [0] * (L+1)
        slotidx[ 0] = 1
        slotidx[-1] = 1
        opslots = [[]] * len(opchains)
        for j, opc in enumerate(opchains):
            opslots[j] = [0] * opc.length
            for i in range(opc.length-1):
                k = opc.istart + i + 1
                opslots[j][i] = slotidx[k]
                slotidx[k] += 1
            # last slot is 0 (for trailing identity matrices)

        # allocate and fill MPO tensors and corresponding quantum numbers
        op = cls(qd, [np.zeros(slotidx[j], dtype=int) for j in range(L+1)], fill=0j)
        for j, opc in enumerate(opchains):
            for i in range(opc.length):
                if i==0:
                    if opc.istart == 0:
                        k = 0
                    else:
                        k = opslots[maxidxS][opc.istart-1]
                else:
                    k = opslots[j][i-1]
                # add to A (instead of simply assigning) to handle sum of single-site operators without dedicated bond slots
                op.A[opc.istart + i][:, :, k, opslots[j][i]] += opc.oplist[i]
                if opc.length > 1:
                    op.qD[opc.istart + i + 1][opslots[j][i]] = (opc.qD[i] if i < opc.length-1 else 0)

        # consistency check
        for i in range(L):
            assert is_qsparse(op.A[i], [op.qd, -op.qd, op.qD[i], -op.qD[i+1]]), \
                'sparsity pattern of MPO tensor does not match quantum numbers'
        return op

    @property
    def nsites(self) -> int:
        """
        Number of lattice sites.
        """
        return len(self.A)

    @property
    def bond_dims(self) -> list:
        """
        Virtual bond dimensions.
        """
        if len(self.A) == 0:
            return []
        else:
            D = [self.A[i].shape[2] for i in range(len(self.A))]
            D.append(self.A[-1].shape[3])
            return D

    def zero_qnumbers(self):
        """
        Set all quantum numbers to zero (effectively disabling them).
        """
        self.qd.fill(0)
        for i in range(len(self.qD)):
            self.qD[i].fill(0)
        # enable chaining
        return self

    def orthonormalize(self, mode='left'):
        """
        Left- or right-orthonormalize the MPO (Frobenius norm) using QR decompositions.
        """
        if len(self.A) == 0:
            return
        if mode == 'left':
            for i in range(len(self.A) - 1):
                self.A[i], self.A[i+1], self.qD[i+1] = local_orthonormalize_left_qr(
                    self.A[i], self.A[i+1], self.qd, self.qD[i:i+2])
            # last tensor
            self.A[-1], T, self.qD[-1] = local_orthonormalize_left_qr(self.A[-1], np.array([[[[1]]]]), self.qd, self.qD[-2:])
            # normalization factor (real-valued since diagonal of R matrix is real)
            assert T.shape == (1, 1, 1, 1)
            nrm = T[0, 0, 0, 0].real
            if nrm < 0:
                # flip sign such that normalization factor is always non-negative
                self.A[-1] = -self.A[-1]
                nrm = -nrm
            return nrm
        elif mode == 'right':
            for i in reversed(range(1, len(self.A))):
                self.A[i], self.A[i-1], self.qD[i] = local_orthonormalize_right_qr(
                    self.A[i], self.A[i-1], self.qd, self.qD[i:i+2])
            # first tensor
            self.A[0], T, self.qD[0] = local_orthonormalize_right_qr(self.A[0], np.array([[[[1]]]]), self.qd, self.qD[:2])
            # normalization factor (real-valued since diagonal of R matrix is real)
            assert T.shape == (1, 1, 1, 1)
            nrm = T[0, 0, 0, 0].real
            if nrm < 0:
                # flip sign such that normalization factor is always non-negative
                self.A[0] = -self.A[0]
                nrm = -nrm
            return nrm
        else:
            raise ValueError(f'mode = {mode} invalid; must be "left" or "right".')

    def as_matrix(self) -> np.ndarray:
        """
        Merge all tensors to obtain the matrix representation on the full Hilbert space.
        """
        op = self.A[0]
        for i in range(1, len(self.A)):
            op = merge_MPO_tensor_pair(op, self.A[i])
        assert op.ndim == 4
        assert op.shape[2] == 1 and op.shape[3] == 1
        op = op.reshape((op.shape[0], op.shape[1]))
        return op

    def __add__(self, other):
        """
        Add MPO to another.
        """
        return add_MPOs(self, other)

    def __sub__(self, other):
        """
        Subtract another MPO.
        """
        return add_MPOs(self, other, alpha=-1)

    def __matmul__(self, other):
        """
        Multiply MPO with another (composition along physical dimension).
        """
        return multiply_MPOs(self, other)


def local_orthonormalize_left_qr(A: np.ndarray, Anext: np.ndarray, qd: Sequence[int], qD: Sequence[Sequence[int]]):
    """
    Left-orthonormalize local site tensor `A` by a QR decomposition,
    and update tensor at next site.
    """
    # perform QR decomposition and replace A by reshaped Q matrix
    s = A.shape
    assert len(s) == 4
    q0 = qnumber_flatten([qd, -qd, qD[0]])
    Q, R, qbond = qr(A.reshape((s[0]*s[1]*s[2], s[3])), q0, qD[1])
    A = Q.reshape((s[0], s[1], s[2], Q.shape[1]))
    # update Anext tensor: multiply with R from left
    Anext = np.tensordot(R, Anext, (1, 2)).transpose((1, 2, 0, 3))
    return (A, Anext, qbond)


def local_orthonormalize_right_qr(A: np.ndarray, Aprev: np.ndarray, qd: Sequence[int], qD: Sequence[Sequence[int]]):
    """
    Right-orthonormalize local site tensor `A` by a QR decomposition,
    and update tensor at previous site.
    """
    # flip left and right virtual bond dimensions
    A = A.transpose((0, 1, 3, 2))
    # perform QR decomposition and replace A by reshaped Q matrix
    s = A.shape
    assert len(s) == 4
    q0 = qnumber_flatten([qd, -qd, -qD[1]])
    Q, R, qbond = qr(A.reshape((s[0]*s[1]*s[2], s[3])), q0, -qD[0])
    A = Q.reshape((s[0], s[1], s[2], Q.shape[1])).transpose((0, 1, 3, 2))
    # update Aprev tensor: multiply with R from right
    Aprev = np.tensordot(Aprev, R, (3, 1))
    return (A, Aprev, -qbond)


def merge_MPO_tensor_pair(A0: np.ndarray, A1: np.ndarray) -> np.ndarray:
    """
    Merge two neighboring MPO tensors.
    """
    A = np.einsum(A0, (0, 2, 4, 6), A1, (1, 3, 6, 5), (0, 1, 2, 3, 4, 5), optimize=True)
    # combine original physical dimensions
    s = A.shape
    A = A.reshape((s[0]*s[1], s[2]*s[3], s[4], s[5]))
    return A


def add_MPOs(op0: MPO, op1: MPO, alpha=1) -> MPO:
    """
    Logical addition of two MPOs (effectively sum virtual bond dimensions)
    with the second MPO scaled by 'alpha'.
    """
    # number of lattice sites must agree
    assert op0.nsites == op1.nsites
    L = op0.nsites
    # physical quantum numbers must agree
    assert np.array_equal(op0.qd, op1.qd)
    d = len(op0.qd)

    # initialize with dummy tensors and bond quantum numbers
    op = MPO(op0.qd, (L+1)*[[0]])

    if L == 1:
        # single site
        # dummy bond quantum numbers must agree
        assert np.array_equal(op0.qD[0], op1.qD[0])
        assert np.array_equal(op0.qD[1], op1.qD[1])
        op.qD[0] = op0.qD[0].copy()
        op.qD[1] = op0.qD[1].copy()
        # simply add MPO tensors
        op.A[0] = op0.A[0] + alpha*op1.A[0]
        # consistency check
        assert is_qsparse(op.A[0], [op.qd, -op.qd, op.qD[0], -op.qD[1]]), \
            'sparsity pattern of MPO tensor does not match quantum numbers'
    elif L > 1:
        # combine virtual bond quantum numbers
        # leading and trailing (dummy) bond quantum numbers must agree
        assert np.array_equal(op0.qD[ 0], op1.qD[ 0])
        assert np.array_equal(op0.qD[-1], op1.qD[-1])
        op.qD[ 0] = op0.qD[ 0].copy()
        op.qD[-1] = op0.qD[-1].copy()
        # intermediate bond quantum numbers
        for i in range(1, L):
            op.qD[i] = np.concatenate((op0.qD[i], op1.qD[i]))

        # leftmost tensor
        op.A[0] = np.block([op0.A[0], alpha*op1.A[0]])
        # intermediate tensors
        for i in range(1, L - 1):
            s0 = op0.A[i].shape
            s1 = op1.A[i].shape
            # form block-diagonal tensor
            op.A[i] = np.block([[op0.A[i], np.zeros((d, d, s0[2], s1[3]))], [np.zeros((d, d, s1[2], s0[3])), op1.A[i]]])
        # rightmost tensor
        op.A[-1] = np.block([[op0.A[-1]], [op1.A[-1]]])

        # consistency check
        for i in range(1, L):
            assert is_qsparse(op.A[i], [op.qd, -op.qd, op.qD[i], -op.qD[i+1]]), \
                'sparsity pattern of MPO tensor does not match quantum numbers'
    return op


def multiply_MPOs(op0: MPO, op1: MPO) -> MPO:
    """
    Multiply two MPOs (composition along physical dimension).
    """
    # number of lattice sites must agree
    assert op0.nsites == op1.nsites
    L = op0.nsites
    # physical quantum numbers must agree
    assert np.array_equal(op0.qd, op1.qd)

    # initialize with dummy tensors and bond quantum numbers
    op = MPO(op0.qd, (L+1)*[[0]])

    # combine virtual bond quantum numbers
    for i in range(L + 1):
        op.qD[i] = qnumber_flatten([op0.qD[i], op1.qD[i]])

    for i in range(L):
        # multiply physical dimensions and reorder dimensions
        op.A[i] = np.tensordot(op0.A[i], op1.A[i], (1, 0)).transpose((0, 3, 1, 4, 2, 5))
        # merge virtual bonds
        s = op.A[i].shape
        assert len(s) == 6
        op.A[i] = op.A[i].reshape((s[0], s[1], s[2]*s[3], s[4]*s[5]))
        # consistency check
        assert is_qsparse(op.A[i], [op.qd, -op.qd, op.qD[i], -op.qD[i+1]]), \
            'sparsity pattern of MPO tensor does not match quantum numbers'
    return op
