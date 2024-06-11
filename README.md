# BOATMAP


## Install

```shell
sudo apt install python3.11
sudo apt install python3.11-venv
python3.11 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Run

```shell
python exmaple.py
```

## Usage

There are two functions that need to be defined in `example.py`.

1. A function to fetch the heart geometry. A dense tetrahedron volume mesh, where each row in `torso_pts` is a xyz locaion of a vertex, `torso_uvc` is the uvc coordinates assocated with each vertex, and each row in `biv_elem` describes a tetrahedron which holds indices into the `torso_pts` and the last colum describes the tissue status (scar, grey zone, healthy), also `biv_elem` is only defined on the left and right ventricle.
```python
def heart_geometry():
    XYZ_COL = ['x', 'y', 'z']
    UVC_COL = ['apicobasal', 'transmural', 'rotational', 'transventricular']
    TETRA_COL = ['a', 'b', 'c', 'd']
    torso_pts = pd.read_csv(DATA_PATH / "geometry/torso.1000um.retag.pts", skiprows=1, names=XYZ_COL, sep=" ")/1000
    torso_uvc = pd.read_csv(DATA_PATH / "geometry/torso.1000um.retag.hpts", skiprows=1, names=UVC_COL, sep=" ")
    biv_elem = pd.read_csv(DATA_PATH / "geometry/biv.elem", skiprows=1, names=TETRA_COL+['tag'], sep=" ")
    return torso_pts, torso_uvc, biv_elem
```

2. A function to simulate an ecg at an index in the `torso_pts` file. The current code assumes the ecgs are precomputed and reads them from the file.
```python
def simulate_ecg_fn(index: int):
    p = DATA_PATH / f"ecg/{index:09}.json"
    j = json.loads(p.read_text())
    # provided ECG must be in this format
    validate(j, schema=schema.ecg)
    return j
```

