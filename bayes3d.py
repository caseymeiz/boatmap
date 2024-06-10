from dataclasses import dataclass, field, asdict
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
import warnings


@dataclass
class Bayes3DConfig:
    kappa: float = field(default=1)
    nu: float = field(default=2.5)
    restarts: int = field(default=10)
    coord_scalar: str = field(default='CenterMax')
    length_scale_bounds: tuple = field(default=(5, 40))


class Bayes3D:
    def __init__(self, config: Bayes3DConfig, domain):
        self.original_domain = domain
        domain = np.array(domain)
        self.scalar = CenterMax()
        self.scalar.fit(domain)
        self.domain = domain
        self.config = config
        self.metrics_data = dict(config=asdict(config), suggest_calls=list())

        self.gp = GaussianProcessRegressor(
            kernel=Matern(
                nu=config.nu,
                length_scale_bounds=(config.length_scale_bounds[0] / self.scalar.max, config.length_scale_bounds[1] / self.scalar.max)
            ),
            alpha=1e-6,
            n_restarts_optimizer=config.restarts,
        )

    def suggest(self, R, s):
        training_indices = R.index
        R = np.array(R)
        s = np.array(s)
        warnings.filterwarnings("ignore")
        self.gp.fit(self.scalar.transform(R), s)
        warnings.filterwarnings("default")

        mean, std = self.gp.predict(self.scalar.transform(self.domain), return_std=True)
        ucb = mean + self.config.kappa * std
        self.metrics_data['suggest_calls'].append(dict(mean=mean, std=std, ucb=ucb))
        for suggest_index in np.argsort(-ucb):
            r = self.original_domain.iloc[[suggest_index]]
            if suggest_index not in training_indices:
                return r, dict(r=r.to_dict(index=True), mean=mean.tolist(), std=std.tolist(), ucb=ucb.tolist(), suggest_index=int(suggest_index))


class CenterMax:
    def __init__(self, scale=1.0):
        self.scale = scale
        self.means_ = None

    def fit(self, X):
        self.means_ = np.mean(X, axis=0)
        coords_centered = X - self.means_
        self.max = np.max(np.abs(coords_centered))
        return self

    def transform(self, coords):
        coords_centered = coords - self.means_
        return coords_centered / self.max

    def fit_transform(self, X):
        return self.fit(X).transform(X)
