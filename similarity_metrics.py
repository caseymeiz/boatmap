import numpy as np


def concat_similarity(qrs_target, qrs):
    def concat(ecg):
        leads = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
        con_ecg = list()
        for lead in leads:
            con_ecg.extend(ecg['ecg'][lead])
        return np.array(con_ecg)
    qrs_tgt_con = concat(qrs_target)
    qrs_con = concat(qrs)
    return np.corrcoef(qrs_tgt_con, qrs_con)[0][1]

