import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.linear_model._ridge import GridSearchCV, Ridge, LinearModel


class CustomRidgeCV(LinearModel):
    """
    Custom RidgeCV made from _BaseRidgeCV.
    I left only K-fold CV option and added storing of CV values for it,
    and changed some of default parameters.
    Everything else is the same as in regular RidgeCV.
    """

    def __init__(self, alphas=(0.1, 1.0, 10.0),
                 fit_intercept=True, normalize=False,
                 scoring='neg_mean_squared_error', cv=3,  # изменено
                 gcv_mode=None,
                 store_cv_values=True):  # изменено
        self.alphas = np.asarray(alphas)
        self.fit_intercept = fit_intercept
        self.normalize = normalize

        self.scoring = scoring

        self.cv = cv
        self.gcv_mode = gcv_mode
        self.store_cv_values = store_cv_values

        self.cv_values_ = None
        self.alpha_ = None
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y, sample_weight=None):
        """Fit Ridge regression model with cv.
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Training data. If using GCV, will be cast to float64
            if necessary.
        y : ndarray of shape (n_samples,) or (n_samples, n_targets)
            Target values. Will be cast to X's dtype if necessary.
        sample_weight : float or ndarray of shape (n_samples,), default=None
            Individual weights for each sample. If given a float, every sample
            will have the same weight.
        Returns
        -------
        self : object
        Notes
        -----
        When sample_weight is provided, the selected hyperparameter may depend
        on whether we use generalized cross-validation (cv=None or cv='auto')
        or another form of cross-validation, because only generalized
        cross-validation takes the sample weights into account when computing
        the validation score.
        """
        cv = self.cv
        if cv is None:
            raise ValueError('Expected number of folds of type int')
            # estimator = _RidgeGCV(self.alphas,
            #                       fit_intercept=self.fit_intercept,
            #                       normalize=self.normalize,
            #                       scoring=self.scoring,
            #                       gcv_mode=self.gcv_mode,
            #                       store_cv_values=self.store_cv_values)
            # estimator.fit(X, y, sample_weight=sample_weight)
            # self.alpha_ = estimator.alpha_
            # if self.store_cv_values:
            #     self.cv_values_ = estimator.cv_values_
        else:
            # if self.store_cv_values:
            #     raise ValueError("cv!=None and store_cv_values=True "
            #                      " are incompatible")
            parameters = {'alpha': self.alphas}
            solver = 'sparse_cg' if sparse.issparse(X) else 'auto'
            gs = GridSearchCV(Ridge(fit_intercept=self.fit_intercept,
                                    normalize=self.normalize,
                                    solver=solver),
                              parameters, scoring=self.scoring, cv=self.cv,
                              return_train_score=False, error_score=0)  # изменено

            gs.fit(X, y, sample_weight=sample_weight)
            estimator = gs.best_estimator_
            self.alpha_ = gs.best_estimator_.alpha

            # дописано
            if self.store_cv_values:
                cv_results = pd.DataFrame(gs.cv_results_)

                def get_scores_for_param(res, n_fold):
                    scores = [res[f'split{n}_test_score'] for n in range(n_fold)]
                    return {"param_value": res['param_alpha'],
                            "scores": scores,
                            "mean_mse": abs(sum(scores) / len(scores))}

                self.cv_values_ = [get_scores_for_param(res, self.cv) for _, res in cv_results.iterrows()]

        self.coef_ = estimator.coef_
        self.intercept_ = estimator.intercept_

        return self
