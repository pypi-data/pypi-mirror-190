from bbcpy.functions.statistics import cov
import numpy as np
from scipy.linalg import eigh
from sklearn.base import ClassifierMixin, TransformerMixin, BaseEstimator
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.multiclass import unique_labels
from pyriemann.utils import covariance
from pyriemann.stats import mean_covariance


class Wishart(BaseEstimator, ClassifierMixin, TransformerMixin):
    def __init__(self, estimator=covariance._scm, excllev=None, autobias=False, geomean=False, covupdate=False):
        self.estimator = estimator
        self.excllev = excllev
        self.autobias = autobias
        self.geomean = geomean
        self.covupdate = covupdate

    def fit(self, X, y=None):
        """

        :param X: epoched data
        :param y: class-label
        :return:
        """
        if y is not None:
            X.y = y
            X.mrk.y = y
        self.classes_ = unique_labels(y)
        Sigma_trial = cov(X, target='trial')
        if self.geomean:
            self.Sigma_ = [mean_covariance(Sigma_trial[y == 0]), mean_covariance(Sigma_trial[y == 1])]
        elif self.excllev is not None:
            covtr = np.trace(np.linalg.pinv(cov(X, target='all', estimator=self.estimator)) @ Sigma_trial, axis1=1,
                             axis2=2) / X.shape[1]
            sel_tr = covtr <= self.excllev
            self.Sigma_ = cov(X[sel_tr], target='class', estimator=self.estimator)
        else:
            self.Sigma_ = cov(X, target='class', estimator=self.estimator)
        # self.SigmaA_ = cov(X, target='all', estimator=self.estimator)
        self.Sigmainv_ = [np.linalg.pinv(self.Sigma_[0]), np.linalg.pinv(self.Sigma_[1])]

        if self.autobias:
            wx = (np.trace(self.Sigmainv_[0] @ Sigma_trial, axis1=1, axis2=2) - np.trace(
                self.Sigmainv_[1] @ Sigma_trial, axis1=1, axis2=2))
            self.b_ = - wx.mean()
        else:
            self.b_ = (np.log(np.linalg.det(self.Sigma_[0])) - np.log(np.linalg.det(self.Sigma_[1])))
            self.b_v_ = np.concatenate([(np.log(np.linalg.det(self.Sigma_[0])), np.log(np.linalg.det(self.Sigma_[1])))])
        return self

    def transform(self, X):
        """
        :param X: ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        :param y: ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        :return: out : ndarray, shape (n_matrices, n_csp, n_time)
            transformed
        """
        check_is_fitted(self)
        n = X.shape[2]
        Sigma = cov(X, target='trial')
        wx = np.concatenate([(np.trace(self.Sigmainv_[0] @ Sigma, axis1=1, axis2=2), np.trace(self.Sigmainv_[1] @ Sigma,
                                                                                              axis1=1, axis2=2))])
        return (n - 1) * wx.T + n * self.b_v_

    def decision_function(self, X):
        """
        Predict confidence scores for samples.
        The confidence score for a sample is proportional to the signed
        distance of that sample to the hyperplane.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the confidence scores.
        Returns
        -------
        scores : ndarray of shape (n_samples,) or (n_samples, n_classes)
            Confidence scores per `(n_samples, n_classes)` combination. In the
            binary case, confidence score for `self.classes_[1]` where >0 means
            this class would be predicted.
        """
        check_is_fitted(self)
        n = X.shape[2]
        Sigma = cov(X, target='trial')
        wx = (np.trace(self.Sigmainv_[0] @ Sigma, axis1=1, axis2=2) - np.trace(self.Sigmainv_[1] @ Sigma, axis1=1,
                                                                               axis2=2))
        y = (n - 1) * wx + n * self.b_
        if self.covupdate:
            # deltaS = cov(X, target='all', estimator=self.estimator) - self.SigmaA_
            # Sigma = Sigma - deltaS
            y = y - (n - 1) * np.trace(
                (self.Sigmainv_[0] - self.Sigmainv_[1]) @ np.mean(Sigma, axis=0),
                axis1=0, axis2=1)

        return y

    def predict(self, X):
        """
        Predict class labels for samples in X.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the predictions.
        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Vector containing the class labels for each sample.
        """
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = scores.argmax(axis=1)
        return self.classes_[indices]


class Miklodyfire(BaseEstimator, ClassifierMixin, TransformerMixin):
    def __init__(self, n_cmps=6, estimator=covariance._scm, excllev=None, autobias=False):
        self.n_cmps = n_cmps
        self.estimator = estimator
        self.excllev = excllev
        self.autobias = autobias

    def fit(self, X, y=None):
        """

        :param X: epoched data
        :param y: class-label
        :return:
        """
        if y is not None:
            X.y = y
            X.mrk.y = y
        self.classes_ = unique_labels(y)
        Sigma_trial = cov(X, target='trial')
        if self.excllev is not None:
            covtr = np.trace(np.linalg.pinv(cov(X, target='all', estimator=self.estimator)) @ Sigma_trial, axis1=1,
                             axis2=2) / X.shape[1]
            sel_tr = covtr <= self.excllev
            self.Sigma_ = cov(X[sel_tr], target='class', estimator=self.estimator)
        else:
            self.Sigma_ = cov(X, target='class', estimator=self.estimator)
        # d, W = eigh(np.linalg.pinv(self.Sigma_[0])-np.linalg.pinv(self.Sigma_[1]),
        ##                      np.linalg.pinv(self.Sigma_[0])+np.linalg.pinv(self.Sigma_[1])/2)
        d, W = eigh(self.Sigma_[0] - self.Sigma_[1], (self.Sigma_[0] + self.Sigma_[1]) / 2)
        # selected_csps = np.flipud(np.argsort(np.maximum(d, 1 - d)))[:self.n_cmps]
        selected_csps = np.flipud(np.argsort(np.abs(d)))[:self.n_cmps]
        self.W = W[:, selected_csps]
        self.d = d[selected_csps]
        self.Sigma_ = [self.W.T @ self.Sigma_[0] @ self.W, self.W.T @ self.Sigma_[1] @ self.W]
        # self.Sigmainv_ = W[:, selected_csps] @ np.diag(d[selected_csps]) @ W[:, selected_csps].T
        # self.Sigmainv_ = [W[:, selected_csps].T @ np.linalg.pinv(self.Sigma_[0])  W[:, selected_csps],
        #     W[:, selected_csps].T @ np.linalg.pinv(self.Sigma_[1]) @ W[:, selected_csps]]
        self.Sigmainv_ = [np.linalg.pinv(self.Sigma_[0]), np.linalg.pinv(self.Sigma_[1])]

        if self.autobias:
            Sigma = self.W.T @ Sigma_trial @ self.W
            wx = (np.trace(self.Sigmainv_[0] @ Sigma, axis1=1, axis2=2) - np.trace(self.Sigmainv_[1] @ Sigma,
                                                                                   axis1=1, axis2=2))
            self.b_ = - wx.mean()
        else:

            self.b_ = (np.log(np.linalg.det(self.Sigma_[0])) - np.log(np.linalg.det(self.Sigma_[1])))
            self.b_v_ = np.concatenate([(np.log(np.linalg.det(self.Sigma_[0])), np.log(np.linalg.det(self.Sigma_[1])))])
        return self

    def transform(self, X):
        """
        :param X: ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        :param y: ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        :return: out : ndarray, shape (n_matrices, n_csp, n_time)
            transformed
        """
        check_is_fitted(self)
        n = X.shape[2]
        Sigma = self.W.T @ cov(X, target='trial') @ self.W

        wx = np.concatenate([(np.trace(self.Sigmainv_[0] @ Sigma, axis1=1, axis2=2), np.trace(self.Sigmainv_[1] @ Sigma,
                                                                                              axis1=1, axis2=2))])
        return (n - 1) * wx.T + n * self.b_v_

    def decision_function(self, X):
        """
        Predict confidence scores for samples.
        The confidence score for a sample is proportional to the signed
        distance of that sample to the hyperplane.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the confidence scores.
        Returns
        -------
        scores : ndarray of shape (n_samples,) or (n_samples, n_classes)
            Confidence scores per `(n_samples, n_classes)` combination. In the
            binary case, confidence score for `self.classes_[1]` where >0 means
            this class would be predicted.
        """
        check_is_fitted(self)
        n = X.shape[2]
        Sigma = self.W.T @ cov(X, target='trial') @ self.W
        wx = (np.trace(self.Sigmainv_[0] @ Sigma, axis1=1, axis2=2) - np.trace(self.Sigmainv_[1] @ Sigma,
                                                                               axis1=1, axis2=2))
        return (n - 1) * wx + n * self.b_

    def predict(self, X):
        """
        Predict class labels for samples in X.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the predictions.
        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Vector containing the class labels for each sample.
        """
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = scores.argmax(axis=1)
        return self.classes_[indices]


class Miklodyfire2(BaseEstimator, ClassifierMixin, TransformerMixin):
    def __init__(self, n_cmps=6, estimator=covariance._scm, excllev=None, autobias=False):
        self.n_cmps = n_cmps
        self.estimator = estimator
        self.excllev = excllev
        self.autobias = autobias

    def fit(self, X, y=None):
        """

        :param X: epoched data
        :param y: class-label
        :return:
        """
        if y is not None:
            X.y = y
            X.mrk.y = y
        self.classes_ = unique_labels(y)
        n = X.shape[2]
        Sigma_trial = cov(X, target='trial')
        if self.excllev is not None:
            covtr = np.trace(np.linalg.pinv(cov(X, target='all', estimator=self.estimator)) @ Sigma_trial, axis1=1,
                             axis2=2) / X.shape[1]
            sel_tr = covtr <= self.excllev
            self.Sigma_ = cov(X[sel_tr], target='class', estimator=self.estimator)
        else:
            self.Sigma_ = cov(X, target='class', estimator=self.estimator)
        d, W = eigh(np.linalg.pinv(self.Sigma_[0]) - np.linalg.pinv(self.Sigma_[1]))
        # d, W = eigh(self.Sigma_[0] - self.Sigma_[1], (self.Sigma_[0] + self.Sigma_[1]) / 2)
        selected_csps = np.flipud(np.argsort(np.abs(d)))[:self.n_cmps]
        self.W = W[:, selected_csps]
        self.d = d[selected_csps]
        self.Sigmainv_ = self.W @ np.diag(self.d) @ self.W.T

        if self.autobias:
            wx = np.trace(self.Sigmainv_ @ Sigma_trial, axis1=1, axis2=2)
            self.b_ = - (n - 1) / n * wx.mean()
            # out = (n - 1) * wx - n * wx.mean()
            # self.b_ = np.mean((n-1)/n * wx - 1/n * out)
        else:
            # self.b_ = - np.log(np.prod(self.d))
            # self.b_ = np.log(np.linalg.det(np.eye(X.shape[1])-self.Sigma_[0] @ self.Sigmainv_))
            # self.b_ = (np.log(np.linalg.det(self.Sigma_[0])) - np.log(np.linalg.det(self.Sigma_[1])))
            self.b_ = (np.log(np.linalg.det(self.W.T @ self.Sigma_[0] @ self.W)) -
                       np.log(np.linalg.det(self.W.T @ self.Sigma_[1] @ self.W)))
        return self

    def transform(self, X):
        """
        :param X: ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        :param y: ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        :return: out : ndarray, shape (n_matrices, n_csp, n_time)
            transformed
        """
        return X

    def decision_function(self, X):
        """
        Predict confidence scores for samples.
        The confidence score for a sample is proportional to the signed
        distance of that sample to the hyperplane.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the confidence scores.
        Returns
        -------
        scores : ndarray of shape (n_samples,) or (n_samples, n_classes)
            Confidence scores per `(n_samples, n_classes)` combination. In the
            binary case, confidence score for `self.classes_[1]` where >0 means
            this class would be predicted.
        """
        check_is_fitted(self)
        n = X.shape[2]
        Sigma = cov(X, target='trial')
        wx = np.trace(self.Sigmainv_ @ Sigma, axis1=1, axis2=2)
        return (n - 1) * wx + n * self.b_

    def predict(self, X):
        """
        Predict class labels for samples in X.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the predictions.
        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Vector containing the class labels for each sample.
        """
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = scores.argmax(axis=1)
        return self.classes_[indices]


class Miklodyfire3(BaseEstimator, ClassifierMixin, TransformerMixin):
    def __init__(self, n_cmps=6, estimator=covariance._scm, excllev=None, autobias=False):
        self.n_cmps = n_cmps
        self.estimator = estimator
        self.excllev = excllev
        self.autobias = autobias

    def fit(self, X, y=None):
        """

        :param X: epoched data
        :param y: class-label
        :return:
        """
        if y is not None:
            X.y = y
            X.mrk.y = y
        self.classes_ = unique_labels(y)
        n = X.shape[2]
        Sigma_trial = cov(X, target='trial')
        if self.excllev is not None:
            covtr = np.trace(np.linalg.pinv(cov(X, target='all', estimator=self.estimator)) @ Sigma_trial, axis1=1,
                             axis2=2) / X.shape[1]
            sel_tr = covtr <= self.excllev
            self.Sigma_ = cov(X[sel_tr], target='class', estimator=self.estimator)
        else:
            self.Sigma_ = cov(X, target='class', estimator=self.estimator)
        d, W = eigh(cov(X, target='all', estimator=self.estimator))
        d1 = np.diag(W.T @ self.Sigma_[0] @ W)
        d2 = np.diag(W.T @ self.Sigma_[1] @ W)
        selected_csps = np.flipud(np.argsort(np.abs(np.log(d1) - np.log(d2))))[:self.n_cmps]
        self.W = W[:, selected_csps]
        # self.d = d[selected_csps]
        self.Sigmainv_ = self.W @ np.diag(1 / d1[selected_csps]) @ self.W.T - self.W @ np.diag(
            1 / d2[selected_csps]) @ self.W.T

        if self.autobias:
            wx = np.trace(self.Sigmainv_ @ Sigma_trial, axis1=1, axis2=2)
            self.b_ = - (n - 1) / n * wx.mean()
            # out = (n - 1) * wx - n * wx.mean()
            # self.b_ = np.mean((n-1)/n * wx - 1/n * out)
        else:
            self.b_ = - np.log(np.prod(np.concatenate([d1[selected_csps], 1 / d2[selected_csps]])))
            # self.b_ = - np.log(np.prod(np.concatenate([self.W @ np.diag(d1[selected_csps]) @ self.W.T,
            #                                           self.W @ np.diag(1/d2[selected_csps]) @ self.W.T])))
            # self.b_ = np.log(np.linalg.det(np.eye(X.shape[1])-self.Sigma_[0] @ self.Sigmainv_))
            # self.b_ = (np.log(np.linalg.det(self.Sigma_[0])) - np.log(np.linalg.det(self.Sigma_[1])))
            # self.b_ = (np.log(np.linalg.det(self.W.T @ self.Sigma_[0] @ self.W)) -
            #           np.log(np.linalg.det(self.W.T @ self.Sigma_[1] @ self.W)))
        return self

    def transform(self, X):
        """
        :param X: ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        :param y: ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        :return: out : ndarray, shape (n_matrices, n_csp, n_time)
            transformed
        """
        return X

    def decision_function(self, X):
        """
        Predict confidence scores for samples.
        The confidence score for a sample is proportional to the signed
        distance of that sample to the hyperplane.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the confidence scores.
        Returns
        -------
        scores : ndarray of shape (n_samples,) or (n_samples, n_classes)
            Confidence scores per `(n_samples, n_classes)` combination. In the
            binary case, confidence score for `self.classes_[1]` where >0 means
            this class would be predicted.
        """
        check_is_fitted(self)
        n = X.shape[2]
        Sigma = cov(X, target='trial')
        wx = np.trace(self.Sigmainv_ @ Sigma, axis1=1, axis2=2)
        return (n - 1) * wx + n * self.b_

    def predict(self, X):
        """
        Predict class labels for samples in X.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The data matrix for which we want to get the predictions.
        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Vector containing the class labels for each sample.
        """
        scores = self.decision_function(X)
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = scores.argmax(axis=1)
        return self.classes_[indices]
