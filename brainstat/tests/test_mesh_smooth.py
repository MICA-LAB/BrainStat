import numpy as np
import pickle
from .testutil import datadir
from brainstat.mesh.data import mesh_smooth


def dummy_test(infile, expfile):

    # load input test data
    ifile = open(infile, "br")
    idic = pickle.load(ifile)
    ifile.close()

    Y = idic["Y"]
    FWHM = idic["FWHM"]

    surf = {}
    if "tri" in idic.keys():
        surf["tri"] = idic["tri"]

    if "lat" in idic.keys():
        surf["lat"] = idic["lat"]

    # run mesh_smooth
    Y_out = mesh_smooth(Y, surf, FWHM)

    # load expected outout data
    efile = open(expfile, "br")
    expdic = pickle.load(efile)
    efile.close()
    Y_exp = expdic["Python_Y"]

    testout = []

    comp = np.allclose(Y_out, Y_exp, rtol=1e-05, equal_nan=True)
    testout.append(comp)

    assert all(flag == True for (flag) in testout)


def test_01():
    infile = datadir("xstatsmo_01_IN.pkl")
    expfile = datadir("xstatsmo_01_OUT.pkl")
    dummy_test(infile, expfile)


def test_02():
    infile = datadir("xstatsmo_02_IN.pkl")
    expfile = datadir("xstatsmo_02_OUT.pkl")
    dummy_test(infile, expfile)


def test_03():
    infile = datadir("xstatsmo_03_IN.pkl")
    expfile = datadir("xstatsmo_03_OUT.pkl")
    dummy_test(infile, expfile)


def test_04():
    infile = datadir("xstatsmo_04_IN.pkl")
    expfile = datadir("xstatsmo_04_OUT.pkl")
    dummy_test(infile, expfile)


def test_05():
    infile = datadir("xstatsmo_05_IN.pkl")
    expfile = datadir("xstatsmo_05_OUT.pkl")
    dummy_test(infile, expfile)


def test_06():
    infile = datadir("xstatsmo_06_IN.pkl")
    expfile = datadir("xstatsmo_06_OUT.pkl")
    dummy_test(infile, expfile)


def test_07():
    infile = datadir("xstatsmo_07_IN.pkl")
    expfile = datadir("xstatsmo_07_OUT.pkl")
    dummy_test(infile, expfile)


def test_08():
    infile = datadir("xstatsmo_08_IN.pkl")
    expfile = datadir("xstatsmo_08_OUT.pkl")
    dummy_test(infile, expfile)


def test_09():
    infile = datadir("xstatsmo_09_IN.pkl")
    expfile = datadir("xstatsmo_09_OUT.pkl")
    dummy_test(infile, expfile)


def test_10():
    infile = datadir("xstatsmo_10_IN.pkl")
    expfile = datadir("xstatsmo_10_OUT.pkl")
    dummy_test(infile, expfile)


def test_11():
    infile = datadir("xstatsmo_11_IN.pkl")
    expfile = datadir("xstatsmo_11_OUT.pkl")
    dummy_test(infile, expfile)


def test_12():
    infile = datadir("xstatsmo_12_IN.pkl")
    expfile = datadir("xstatsmo_12_OUT.pkl")
    dummy_test(infile, expfile)
