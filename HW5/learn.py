import numpy as np
from model import CustomRidgeCV
from sklearn.utils.extmath import safe_sparse_dot


class Train:

    def __init__(self, data, target, n_folds, fit_intercept, l2_coef):
        self.data = data
        self.target = target
        self.n_folds = n_folds
        self.fit_intercept = fit_intercept
        self.l2_coef = l2_coef

        y = self.data[self.target]
        x = self.data.drop(columns=[self.target])

        model = CustomRidgeCV(alphas=self.l2_coef, fit_intercept=self.fit_intercept,
                              cv=self.n_folds, store_cv_values=True)
        model.fit(x.values, y.values)

        self.intercept = model.intercept_
        self.coef = {var: coef for var, coef in zip(x.columns.values, model.coef_)}
        self.cv_results = model.cv_values_

    @property
    def model_info(self):
        return {
            "model": {"intercept": self.intercept,
                      "coef": self.coef
                      },

            "cv_results": [{"param_value": res['param_value'],
                            "mean_mse": res['mean_mse'], } for res in self.cv_results]
        }


class Predict:

    def __init__(self, found, data):
        self.model = found.model
        self.intercept = self.model['intercept']
        self.coef = self.model['coef']
        self.data = data

        sorted_model = np.array([self.coef[f] for f in data.columns.values])

        result = safe_sparse_dot(data, sorted_model, dense_output=True) \
            + self.intercept

        self._results = result.tolist()

    @property
    def results_(self):
        return self._results
