import numpy as np
import pickle
from .testutil import datadir
from ..stats import stat_threshold
import gzip


def dummy_test(infile, expfile):

    # load input test data
    with gzip.open(infile, 'rb') as f:
        idic = pickle.load(f)

    # run stat_threshold
    A, B, C, D, E, F = stat_threshold(idic["search_volume"],
                                      idic["num_voxels"],
                                      idic["fwhm"],
                                      idic["df"],
                                      idic["p_val_peak"],
                                      idic["cluster_threshold"],
                                      idic["p_val_extent"],
                                      idic["nconj"],
                                      idic["nvar"],
                                      None,
                                      None,
                                      idic["nprint"])
    outdic = {"peak_threshold": A, "extent_threshold": B,
              "peak_threshold_1": C, "extent_threshold_1": D,
              "t": E, "rho": F}

    # load expected outout data
    with gzip.open(expfile, 'rb') as f:
        expdic = pickle.load(f)

    testout = []

    for key in outdic.keys():
        comp = np.allclose(outdic[key], expdic[key],
                           rtol=1e-05, equal_nan=True)
        testout.append(comp)

    assert all(flag == True for (flag) in testout)


def test_01():
    infile = datadir('thresh_01_IN.pkl.gz')
    expfile = datadir('thresh_01_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_02():
    infile = datadir('thresh_02_IN.pkl.gz')
    expfile = datadir('thresh_02_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_03():
    infile = datadir('thresh_03_IN.pkl.gz')
    expfile = datadir('thresh_03_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_04():
    infile = datadir('thresh_04_IN.pkl.gz')
    expfile = datadir('thresh_04_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_05():
    infile = datadir('thresh_05_IN.pkl.gz')
    expfile = datadir('thresh_05_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_06():
    infile = datadir('thresh_06_IN.pkl.gz')
    expfile = datadir('thresh_06_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_07():
    infile = datadir('thresh_07_IN.pkl.gz')
    expfile = datadir('thresh_07_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_08():
    infile = datadir('thresh_08_IN.pkl.gz')
    expfile = datadir('thresh_08_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_09():
    infile = datadir('thresh_09_IN.pkl.gz')
    expfile = datadir('thresh_09_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_10():
    infile = datadir('thresh_10_IN.pkl.gz')
    expfile = datadir('thresh_10_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_11():
    infile = datadir('thresh_11_IN.pkl.gz')
    expfile = datadir('thresh_11_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_12():
    infile = datadir('thresh_12_IN.pkl.gz')
    expfile = datadir('thresh_12_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_13():
    infile = datadir('thresh_13_IN.pkl.gz')
    expfile = datadir('thresh_13_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_14():
    infile = datadir('thresh_14_IN.pkl.gz')
    expfile = datadir('thresh_14_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_15():
    infile = datadir('thresh_15_IN.pkl.gz')
    expfile = datadir('thresh_15_OUT.pkl.gz')
    dummy_test(infile, expfile)


def test_16():
    infile = datadir('thresh_16_IN.pkl.gz')
    expfile = datadir('thresh_16_OUT.pkl.gz')
    dummy_test(infile, expfile)
