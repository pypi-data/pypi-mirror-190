from functools import partial

import numpy as np
from sklearn.model_selection._split import _BaseKFold
from sklearn.utils.validation import _num_samples
from sklearn.metrics import (
    r2_score,
    median_absolute_error,
    max_error,
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    mean_poisson_deviance,
    mean_gamma_deviance,
    accuracy_score,
    top_k_accuracy_score,
    roc_auc_score,
    average_precision_score,
    log_loss,
    balanced_accuracy_score,
    explained_variance_score,
    brier_score_loss,
    mean_absolute_percentage_error,
)


class TrialWiseKFold(_BaseKFold):
    """Trial wise KFold cross-validator

        Provides train/test indices to split data in train/test sets. Split
        dataset into k consecutive folds (without shuffling by default) to
        achieve an equal number of movement trials in each split.
        Each fold is then used once as a validation while the k - 1 remaining
        folds form the training set.
    """

    def __init__(self, n_splits=5, *, shuffle=False, random_state=None):
        super().__init__(n_splits=n_splits, shuffle=shuffle,
                         random_state=random_state)

    def _iter_test_indices(self, X, y, groups=None):
        n_samples = _num_samples(X)
        indices = np.arange(n_samples)

        labeldiff = np.argwhere(np.diff(y) != 0)[:, 0] + 1
        labeldiff = np.insert(labeldiff, 0, 0)
        labeldiff = np.append(labeldiff, n_samples)

        ld_low = labeldiff[::2]
        ld_high = labeldiff[1::2]

        idx_low = ld_low[
            np.floor(np.linspace(0, len(ld_low) - 1,
                                 self.n_splits + 1)).astype(int)]
        idx_up = ld_high[np.floor(
            np.linspace(0, len(ld_high) - 1, self.n_splits + 1)).astype(int)]

        cv_indices = (idx_low + idx_up) // 2
        cv_indices[0] = 0
        cv_indices[-1] = n_samples
        for i in range(self.n_splits):
            yield indices[cv_indices[i]:cv_indices[i + 1]]


def make_scorer(estimator, X, y, error_score, **kwargs):
    """Create label transforming pipeline scorer.

    Parameters
    ----------
    estimator : scikit-lean pipeline
    X : input data
    y : input labels
    error_score : callable
        error score method
    kwargs
        kwargs passed to error score method

    Returns
    -------
    scorer : callable
        scorer that transforms the labels before comparing y_true and y_pred
    """
    Xt, y_true = estimator[:-1].transform(X, y)
    y_pred = estimator[-1].predict(Xt)
    return error_score(y_true, y_pred, **kwargs)


# Standard regression scores
explained_variance_scorer = partial(make_scorer,
                                    error_score=explained_variance_score)
r2_scorer = partial(make_scorer, error_score=r2_score)
max_error_scorer = partial(make_scorer, error_score=max_error,
                           greater_is_better=False)
neg_mean_squared_error_scorer = partial(make_scorer,
                                        error_score=mean_squared_error,
                                        greater_is_better=False)
neg_mean_squared_log_error_scorer = partial(make_scorer,
                                            error_score=mean_squared_log_error,
                                            greater_is_better=False
)
neg_mean_absolute_error_scorer = partial(make_scorer,
                                         error_score=mean_absolute_error,
                                         greater_is_better=False
)
neg_mean_absolute_percentage_error_scorer = partial(
    make_scorer, error_score=mean_absolute_percentage_error,
    greater_is_better=False
)
neg_median_absolute_error_scorer = partial(make_scorer,
                                           error_score=median_absolute_error,
                                           greater_is_better=False
)
neg_root_mean_squared_error_scorer = partial(make_scorer,
                                             error_score=mean_squared_error,
                                             greater_is_better=False,
                                             squared=False
)
neg_mean_poisson_deviance_scorer = partial(make_scorer,
                                           error_score=mean_poisson_deviance,
                                           greater_is_better=False
)

neg_mean_gamma_deviance_scorer = partial(make_scorer,
                                         error_score=mean_gamma_deviance,
                                         greater_is_better=False
)

# Standard Classification Scores
accuracy_scorer = partial(make_scorer, error_score=accuracy_score)
balanced_accuracy_scorer = partial(make_scorer,
                                   error_score=balanced_accuracy_score)

# Score functions that need decision values
top_k_accuracy_scorer = partial(make_scorer,
                                error_score=top_k_accuracy_score,
                                greater_is_better=True,
                                needs_threshold=True
)
roc_auc_scorer = partial(make_scorer,
                         error_score=roc_auc_score,
                         greater_is_better=True,
                         needs_threshold=True
)
average_precision_scorer = partial(make_scorer,
                                   error_score=average_precision_score,
                                   needs_threshold=True)
roc_auc_ovo_scorer = partial(make_scorer, error_score=roc_auc_score,
                             needs_proba=True,
                                 multi_class="ovo")
roc_auc_ovo_weighted_scorer = partial(make_scorer,
                                      error_score=roc_auc_score,
                                      needs_proba=True,
                                      multi_class="ovo",
                                      average="weighted"
)
roc_auc_ovr_scorer = partial(make_scorer, error_score=roc_auc_score,
                             needs_proba=True,
                                 multi_class="ovr")
roc_auc_ovr_weighted_scorer = partial(make_scorer,
                                      error_score=roc_auc_score,
                                      needs_proba=True,
                                      multi_class="ovr",
                                      average="weighted"
)

# Score function for probabilistic classification
neg_log_loss_scorer = partial(make_scorer,
                              error_score=log_loss,
                              greater_is_better=False,
                              needs_proba=True)
neg_brier_score_scorer = partial(make_scorer,
                                 error_score=brier_score_loss,
                                 greater_is_better=False,
                                 needs_proba=True
)
brier_score_loss_scorer = partial(make_scorer,
                                  error_score=brier_score_loss,
                                  greater_is_better=False,
                                  needs_proba=True
)


SCORERS = dict(
    explained_variance=explained_variance_scorer,
    r2=r2_scorer,
    max_error=max_error_scorer,
    neg_median_absolute_error=neg_median_absolute_error_scorer,
    neg_mean_absolute_error=neg_mean_absolute_error_scorer,
    neg_mean_absolute_percentage_error=neg_mean_absolute_percentage_error_scorer,  # noqa
    neg_mean_squared_error=neg_mean_squared_error_scorer,
    neg_mean_squared_log_error=neg_mean_squared_log_error_scorer,
    neg_root_mean_squared_error=neg_root_mean_squared_error_scorer,
    neg_mean_poisson_deviance=neg_mean_poisson_deviance_scorer,
    neg_mean_gamma_deviance=neg_mean_gamma_deviance_scorer,
    accuracy=accuracy_scorer,
    top_k_accuracy=top_k_accuracy_scorer,
    roc_auc=roc_auc_scorer,
    roc_auc_ovr=roc_auc_ovr_scorer,
    roc_auc_ovo=roc_auc_ovo_scorer,
    roc_auc_ovr_weighted=roc_auc_ovr_weighted_scorer,
    roc_auc_ovo_weighted=roc_auc_ovo_weighted_scorer,
    balanced_accuracy=balanced_accuracy_scorer,
    average_precision=average_precision_scorer,
    neg_log_loss=neg_log_loss_scorer,
    neg_brier_score=neg_brier_score_scorer,
)
