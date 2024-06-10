from dataclasses import dataclass, field
import pandas as pd


@dataclass
class LocalizeConfig:
    init: list = field(default=list)


class Guide:
    def __init__(self, model):
        self.model = model

    def localize(self, ecg_fn, QRS_tgt, similarity_fn, termination_criterion, config):
        R = config.init
        ecgs = [ecg_fn(loc) for loc, r in R.iterrows()]
        s = [similarity_fn(QRS_tgt, ecg) for ecg in ecgs]
        i = 0
        suggest_metrics = list()
        while all((not termination_criterion(QRS_tgt, ecg) for ecg in ecgs)) and len(R) < 50:
            r, m = self.model.suggest(R, s)
            suggest_metrics.append(m)
            ecg = ecg_fn(int(r.index[0]))
            s_i = similarity_fn(QRS_tgt, ecg)
            R = pd.concat([R, r], axis=0)
            s.append(s_i)
            ecgs.append(ecg)
            i += 1
        return R.iloc[-1], dict(QRS_tgt=QRS_tgt, R=R.to_dict(index=True), ecgs=ecgs, s=s, i=i, model=suggest_metrics)
