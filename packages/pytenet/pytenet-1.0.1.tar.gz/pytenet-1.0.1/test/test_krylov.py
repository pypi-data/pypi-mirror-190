import unittest
import numpy as np
from scipy.linalg import expm
import pytenet as ptn


class TestKrylov(unittest.TestCase):

    def test_lanczos_iteration(self):

        n = 256
        numiter = 24

        # random Hermitian matrix
        A = crandn((n, n)) / np.sqrt(n)
        A = 0.5 * (A + A.conj().T)

        # random complex starting vector
        vstart = crandn(n) / np.sqrt(n)

        # simply use A as linear transformation
        alpha, beta, V = ptn.lanczos_iteration(lambda x: A @ x, vstart, numiter)

        # check orthogonality of Lanczos vectors
        self.assertTrue(np.allclose(V.T.conj() @ V, np.identity(numiter), rtol=1e-12),
                        msg='matrix of Lanczos vectors must be orthonormalized')

        # Lanczos vectors must tridiagonalize A
        T = np.diag(alpha) + np.diag(beta, 1) + np.diag(beta, -1)
        self.assertTrue(np.allclose(V.conj().T @ A @ V, T, rtol=1e-12),
                        msg='Lanczos vectors must tridiagonalize A')


    def test_arnoldi_iteration(self):

        n = 256
        numiter = 24

        # random matrix
        A = crandn((n, n))
        # random complex starting vector
        vstart = crandn(n) / np.sqrt(n)

        # simply use A as linear transformation
        H, V = ptn.arnoldi_iteration(lambda x: A @ x, vstart, numiter)

        # check orthogonality of Arnoldi vectors
        self.assertTrue(np.allclose(V.conj().T @ V, np.identity(V.shape[1]), rtol=1e-12),
                        msg='matrix of Arnoldi vectors must be orthonormalized')

        self.assertTrue(np.allclose(V.conj().T @ A @ V, H, rtol=1e-12),
                        msg='Arnoldi vectors must transform A to upper Hessenberg form')


    def test_eigh_krylov(self):

        n = 196
        numiter = 30
        numeig  = 2

        # random Hermitian matrix
        A = crandn((n, n)) / np.sqrt(n)
        A = 0.5 * (A + A.conj().T)

        # random complex starting vector
        vstart = crandn(n) / np.sqrt(n)

        # simply use A as linear transformation;
        w, u_ritz = ptn.eigh_krylov(lambda x: A @ x, vstart, numiter, numeig)

        # check orthogonality of Ritz matrix
        self.assertTrue(np.allclose(u_ritz.conj().T @ u_ritz, np.identity(numeig), rtol=1e-12),
                        msg='matrix of Ritz eigenvectors must be orthonormalized')

        # check U^H A U = diag(w)
        self.assertTrue(np.allclose(u_ritz.conj().T @ A @ u_ritz, np.diag(w), rtol=1e-12),
                        msg='Ritz eigenvectors must diagonalize A within Krylov subspace')

        # reference eigenvalues
        w_ref = np.linalg.eigvalsh(A)

        # compare lowest eigenvalues
        self.assertAlmostEqual(w[0], w_ref[0], delta=0.001,
                               msg='lowest Lanczos eigenvalue should approximate exact eigenvalue')

        self.assertAlmostEqual(w[1], w_ref[1], delta=0.02,
                               msg='second-lowest Lanczos eigenvalue should approximate exact eigenvalue')


    def test_expm_krylov(self):

        n = 320
        numiter = 12
        # time step
        dt = 0.4 + 0.2j

        for hermitian in [True, False]:
            # random complex matrix
            A = crandn((n, n)) / np.sqrt(n)
            if hermitian:
                # symmetrize
                A = 0.5 * (A + A.conj().T)

            # random complex vector
            v = crandn(n) / np.sqrt(n)

            # Krylov subspace approximation of expm(dt*A) @ v
            vt = ptn.expm_krylov(lambda x: A @ x, v, dt, numiter, hermitian=hermitian)

            # reference
            vt_ref = expm(dt*A) @ v

            self.assertTrue(np.allclose(vt, vt_ref, rtol=1e-11),
                            msg='Krylov subspace approximation of expm(dt*A) @ v should match reference')


def crandn(size):
    """
    Draw random samples from the standard complex normal (Gaussian) distribution.
    """
    # 1/sqrt(2) is a normalization factor
    return (np.random.standard_normal(size)
       + 1j*np.random.standard_normal(size)) / np.sqrt(2)


if __name__ == '__main__':
    unittest.main()
