import pandas as pd
import numpy as np
xyz_cols = ['x', 'y', 'z']


def get_error(result):
    target_xyz = pd.DataFrame(result['tgt_xyz'])
    predicted_xyz = pd.DataFrame(result["R"]).iloc[[-1]]
    return np.linalg.norm(target_xyz[xyz_cols].values - predicted_xyz[xyz_cols].values)


def count_pace_sites(result):
    return len(pd.DataFrame(result["R"]))


def search_summary(result):
    return (
        f'Pace sites used: {count_pace_sites(result)}\n'
        f'Prediction error (mm): {get_error(result):.1f}\n'
    )


def search_summary_agg(results):
    return (
        f'Mean Pace sites used: {np.mean([count_pace_sites(r) for r in results])}\n'
        f'Mean Prediction error (mm): {np.mean([get_error(r) for r in results]):.1f}\n'
    )
