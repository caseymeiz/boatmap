# BOATMAP
Paper: https://www.sciencedirect.com/science/article/pii/S0010482524012861

```
@article{meisenzahl_2024,
title = {BOATMAP: Bayesian Optimization Active Targeting for Monomorphic Arrhythmia Pace-mapping},
journal = {Computers in Biology and Medicine},
volume = {182},
pages = {109201},
year = {2024},
issn = {0010-4825},
doi = {https://doi.org/10.1016/j.compbiomed.2024.109201},
author = {Casey Meisenzahl and Karli Gillette and Anton J. Prassl and Gernot Plank and John L. Sapp and Linwei Wang},
}
```

## Component overview

### `bayes3d.py` 

Uses a GP to model to predict the expected similarity between the target ecg and a prospective ecg in a different location on the heart. Has an acquisition function to suggset where to collect the next ecg from.

### `guide.py`
Iteratively fits our surrogate model in `bayes3d.py` and follows the suggested locations to collect ecgs from. The process stops when an ecg collected reaches a similarity threshold that is sufficient.

### `similarity_metrics.py`
Models the similarity between a target ecg and a newly collected ecg.

### `termination_criteria.py`
Predicate to determine if the collected ecg is the predicted location of the target ecg.

### `util.py`
Extracts the coordinates in the provided heart geometry that are viable for pace mapping.

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

