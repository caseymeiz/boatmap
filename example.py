from pathlib import Path
from jsonschema import validate
import json
import schema
from guide import Guide, LocalizeConfig
from similarity_metrics import concat_similarity
from termination_criteria import concat_criterion
import pandas as pd
from bayes3d import Bayes3D, Bayes3DConfig
import analysis
from util import extract_domain_from_heart_geometry
import random

random.seed(42)

DATA_PATH = Path.home() / "cbl/BOATMAP"


def simulate_ecg_fn(index: int):
    p = DATA_PATH / f"ecg/{index:09}.json"
    j = json.loads(p.read_text())
    # provided ECG must be in this format
    validate(j, schema=schema.ecg)
    return j


def heart_geometry():
    XYZ_COL = ['x', 'y', 'z']
    UVC_COL = ['apicobasal', 'transmural', 'rotational', 'transventricular']
    TETRA_COL = ['a', 'b', 'c', 'd']
    torso_pts = pd.read_csv(DATA_PATH / "geometry/torso.1000um.retag.pts", skiprows=1, names=XYZ_COL, sep=" ")/1000
    torso_uvc = pd.read_csv(DATA_PATH / "geometry/torso.1000um.retag.hpts", skiprows=1, names=UVC_COL, sep=" ")
    biv_elem = pd.read_csv(DATA_PATH / "geometry/biv.elem", skiprows=1, names=TETRA_COL+['tag'], sep=" ")
    return torso_pts, torso_uvc, biv_elem


def main():
    torso_pts, torso_uvc, biv_elem = heart_geometry()

    domain_indices = extract_domain_from_heart_geometry(torso_pts, torso_uvc, biv_elem)
    # filter domain to pre-computed ecgs, delete this line if ecgs can be computed on the fly
    domain_indices = list(filter(lambda i: (DATA_PATH / f"ecg/{i:09}.json").exists(), domain_indices))

    ecg_index = random.sample(domain_indices, k=1)[0]
    ecg_target = simulate_ecg_fn(ecg_index)
    domain_xyz = torso_pts.loc[domain_indices]
    guide = Guide(Bayes3D(Bayes3DConfig(), domain_xyz))
    localize_config = LocalizeConfig(init=domain_xyz.loc[random.sample(domain_indices, k=1)])
    predicted_origin, result = guide.localize(simulate_ecg_fn, ecg_target, concat_similarity, concat_criterion, localize_config)
    result = result | dict(tgt_xyz=domain_xyz.loc[[ecg_index]].to_dict(index=True))

    print(analysis.search_summary(result))


if __name__ == "__main__":
    main()

