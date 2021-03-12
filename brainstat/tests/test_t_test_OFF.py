import numpy as np
from scipy.io import loadmat
import pytest
import brainstat.tests.surstat_wrap as sw
from brainstat.stats._t_test import t_test
from brainstat.stats.SLM import SLM
from brainstat.stats.terms import Term

sw.matlab_init_surfstat()


def dummy_test(slm, contrast):

    try:
        # wrap matlab functions
        Wrapped_slm = sw.matlab_T(slm, contrast)

    except:
        pytest.skip("Original MATLAB code does not work with these inputs.")

    # convert input slm-dict into python slm-object
    Python_slm = SLM(Term(1), Term(1))
    for key in slm.keys():
        setattr(Python_slm, key, slm[key])
    setattr(Python_slm, 'contrast', contrast)

    # run python functions
    t_test(Python_slm)

    testout_T = []

    # compare matlab-python outputs
    for key in Wrapped_slm.keys():
        testout_T.append(np.allclose(Wrapped_slm[key],
                                     getattr(Python_slm, key),
                                     rtol=1e-05, equal_nan=True))

    assert all(flag == True for (flag) in testout_T)


# Test 1
def test_01():
    a = np.random.randint(1, 10)
    A = {}
    A['X'] = np.random.rand(a, 1)
    A['df'] = np.array([[3.0]])
    A['coef'] = np.random.rand(1, a).reshape(1, a)
    A['SSE'] = np.random.rand(1, a)
    B = np.random.rand(1).reshape(1, 1)

    dummy_test(A, B)


# Test 2  ### square matrices
def test_02():
    a = np.random.randint(1, 10)
    b = np.random.randint(1, 10)
    A = {}
    A['X'] = np.random.rand(a, a)
    A['df'] = np.array([[b]])
    A['coef'] = np.random.rand(a, a)
    A['SSE'] = np.random.rand(1, a)
    B = np.random.rand(1, a)
    dummy_test(A, B)


# Test 3  ### slm.V & slm.r given
def test_03():
    a = np.array([[4, 4, 4], [5, 5, 5], [6, 6, 6]])
    b = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    Z = np.zeros((3, 3, 2))
    Z[:, :, 0] = a
    Z[:, :, 1] = b
    A = {}
    A['X'] = np.array([[1, 2], [3, 4], [5, 6]])
    A['V'] = Z
    A['df'] = np.array([[1.0]])
    A['coef'] = np.array([[8], [9]])
    A['SSE'] = np.array([[3]])
    A['r'] = np.array([[4]])
    A['dr'] = np.array([[5]])
    B = np.array([[1]])
    dummy_test(A, B)


# Test 4 #### slm.V given, slm.r not
def test_04():
    A = {}
    A['X'] = np.random.rand(3, 2)
    A['V'] = np.array([[4, 4, 4], [5, 5, 5], [6, 6, 6]])
    A['df'] = np.array([np.random.randint(1, 10)])
    A['coef'] = np.random.rand(2, 1)
    A['SSE'] = np.array([np.random.randint(1, 10)])
    A['dr'] = np.array([np.random.randint(1, 10)])
    B = np.array([[1]])
    dummy_test(A, B)


def test_05():
    fname = './data_OFF/thickness_slm.mat'
    f = loadmat(fname)

    slm = {}
    slm['X'] = f['slm']['X'][0, 0]
    slm['df'] = f['slm']['df'][0, 0][0, 0]
    slm['coef'] = f['slm']['coef'][0, 0]
    slm['SSE'] = f['slm']['SSE'][0, 0]
    slm['tri'] = f['slm']['tri'][0, 0]
    slm['resl'] = f['slm']['resl'][0, 0]

    AGE = f['slm']['AGE'][0, 0]

    dummy_test(slm, AGE)


def test_06():
    fname = './data_OFF/thickness_slm.mat'
    f = loadmat(fname)

    slm = {}
    slm['X'] = f['slm']['X'][0, 0]
    slm['df'] = f['slm']['df'][0, 0][0, 0]
    slm['coef'] = f['slm']['coef'][0, 0]
    slm['SSE'] = f['slm']['SSE'][0, 0]
    slm['tri'] = f['slm']['tri'][0, 0]
    slm['resl'] = f['slm']['resl'][0, 0]

    AGE = f['slm']['AGE'][0, 0]

    dummy_test(slm, -1*AGE)


def test_07():
    fname = './data_OFF/thickness.mat'
    f = loadmat(fname)
    A = f['T']
    np.random.shuffle(A)

    AGE = Term(np.array(f['AGE']), 'AGE')
    B = 1 + AGE
    surf = {}
    surf['tri'] = f['tri']
    surf['coord'] = f['coord']

    ### slm = SurfStatLinMod(A, B, surf) ###

    Py_slm = SLM(B, Term(1))
    Py_slm.surf = {"tri": surf["tri"]}
    Py_slm.linear_model(A)

    contrast = np.array(f['AGE']).T

    slm = {}
    slm['X'] = getattr(Py_slm, 'X')
    slm['df'] = getattr(Py_slm, 'df')
    slm['coef'] = getattr(Py_slm, 'coef')
    slm['SSE'] = getattr(Py_slm, 'SSE')
    slm['tri'] = getattr(Py_slm, 'tri')
    slm['resl'] = getattr(Py_slm, 'resl')

    dummy_test(slm, contrast)


def test_08():
    fname = './data_OFF/sofopofo1_slm.mat'
    f = loadmat(fname)
    slm = {}
    slm['X'] = f['slm']['X'][0, 0]
    slm['df'] = f['slm']['df'][0, 0][0, 0]
    slm['coef'] = f['slm']['coef'][0, 0]
    slm['SSE'] = f['slm']['SSE'][0, 0]
    slm['tri'] = f['slm']['tri'][0, 0]
    slm['resl'] = f['slm']['resl'][0, 0]

    contrast = np.random.randint(20, 50, size=(slm['X'].shape[0], 1))

    dummy_test(slm, contrast)


def test_09():
    fname = './data_OFF/sofopofo1.mat'
    f = loadmat(fname)
    T = f['sofie']['T'][0, 0]

    params = f['sofie']['model'][0, 0]
    colnames = ['1', 'ak', 'female', 'male', 'Affect', 'Control1',
                'Perspective', 'Presence', 'ink']

    M = Term(params, colnames)

    SW = {}
    SW['tri'] = f['sofie']['SW'][0, 0]['tri'][0, 0]
    SW['coord'] = f['sofie']['SW'][0, 0]['coord'][0, 0]


    ### slm = SurfStatLinMod(T, M, SW) ###

    Py_slm = SLM(M, Term(1))
    Py_slm.surf = {"tri": SW["tri"]}
    Py_slm.linear_model(T)

    slm = {}
    slm['X'] = getattr(Py_slm, 'X')
    slm['df'] = getattr(Py_slm, 'df')
    slm['coef'] = getattr(Py_slm, 'coef')
    slm['SSE'] = getattr(Py_slm, 'SSE')
    slm['tri'] = getattr(Py_slm, 'tri')
    slm['resl'] = getattr(Py_slm, 'resl')

    contrast = np.random.randint(20, 50, size=(Py_slm.X.shape[0], 1))

    dummy_test(slm, contrast)

