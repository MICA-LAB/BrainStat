import numpy as np
import pickle
from sklearn.model_selection import ParameterGrid
from nilearn import datasets
from brainspace.mesh.mesh_elements import get_cells, get_edges, get_points
from brainspace.vtk_interface.wrappers.data_object import BSPolyData
from brainstat.stats._multiple_comparisons import peak_clus
from brainstat.mesh.utils import mesh_edges
from brainstat.context.utils import read_surface_gz
from testutil import generate_slm, save_slm, datadir, slm2dict


def generate_random_slm(I):
    slm = generate_slm(t = I["t"], df = I["df"],  k = I["k"], resl = I["resl"], 
                       tri = I["tri"], surf = I, dfs = I["dfs"], 
                       mask = I["mask"], cluster_threshold = I["thresh"])
    return slm

def generate_peak_clus_out(slm, I):
    D = {}
    D["peak"], D["clus"], D["clusid"] = peak_clus(slm, I["thresh"],
               reselspvert= I["reselspvert"], edg = I["edg"])
    return D

def params2files(I, D, test_num):
    """Converts params to input/output files"""
    basename = "xstatpeakc"
    fin_name = datadir(basename + "_" + f"{test_num:02d}" + "_IN.pkl")
    fout_name = datadir(basename + "_" + f"{test_num:02d}" + "_OUT.pkl")
    with open(fin_name, "wb") as f:
        pickle.dump(I, f, protocol=4)
    with open(fout_name, "wb") as g:
        pickle.dump(D, g, protocol=4)
    return

np.random.seed(0)

# get some real data
pial_fs5 = datasets.fetch_surf_fsaverage()["pial_left"]
surf = read_surface_gz(pial_fs5)
triangles = np.array(get_cells(surf))

# generate the grid parameters to be looped
mygrid = [{
        "tri" : [np.random.randint(0, int(50), size=(100, 3))],
        "k" : [int(1), int(2)],
        "df" : [None, 1],
        "dfs": [None, 1],
        "cluster_threshold" : [np.random.rand()],
        "mask" : [True],
        "reselspvert" : [None, True],
    },
    {"tri" : [triangles+1], 
     "k" : [1], 
        "df" : [1, np.random.randint(2, 100)],
        "dfs": [1, np.random.randint(2, 100)],
        "cluster_threshold" : [np.random.rand()],
        "mask" : [True],
        "reselspvert" : [None, True],
     }    
]

myparamgrid = ParameterGrid(mygrid)

test_num = 0
for params in myparamgrid:
    I = {}
    # following parameters depend on params["tri"]
    I["tri"] = params["tri"]
    I["edg"] = mesh_edges(params)
    n_edges = I["edg"].shape[0]
    n_vertices = int(I["tri"].shape[0] )
    I["t"] = np.random.random_sample((1, n_vertices))    
    I["resl"] = np.random.random_sample((n_edges, 1))
    if params["mask"] is True:
        I["mask"] = np.random.choice(a=[False, True], size=(n_vertices))
    else:
        I["mask"] = None

    if params["reselspvert"] is True:
        I["reselspvert"] = np.random.rand(n_vertices)
    else:
        I["reselspvert"] = None
    # parameters below don't depend on params["tri"]
    I["k"] = params["k"]   
    I["df"] = params["df"]
    I["dfs"] = params["dfs"]
    I["thresh"] = params["cluster_threshold"]

    # Here we go: generate slm & run peak_clus & save in-out
    slm = generate_random_slm(I)
    D = generate_peak_clus_out(slm, I)    
    test_num += 1
    params2files(I, D, test_num)