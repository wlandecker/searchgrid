import pytest
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.feature_selection import SelectKBest
from searchgrid import set_grid, build_param_grid


@pytest.mark.parametrize(('estimator', 'param_grid'), [
    (set_grid(SVC(), C=[1, 2]),
     {'C': [1, 2]}),
    (set_grid(SVC(), C=[1, 2], gamma=[1, 2]),
     {'C': [1, 2], 'gamma': [1, 2]}),
###    pytest.mark.xfail(
###        (set_grid(SVC(), [{'kernel': ['linear']},
###                          {'kernel': 'rbf', 'gamma': [1, 2]}]),
###         [{'kernel': ['linear']}, {'kernel': 'rbf', 'gamma': [1, 2]}])),
    (make_pipeline(set_grid(SVC(), C=[1, 2], gamma=[1, 2])),
     {'svc__C': [1, 2], 'svc__gamma': [1, 2]}),
###    pytest.mark.xfail(
###        (make_pipeline(set_grid(SVC(), [{'kernel': ['linear']},
###                                        {'kernel': ['rbf'],
###                                         'gamma': [1, 2]}])),
###         [{'svc__kernel': ['linear']},
###          {'svc__kernel': 'rbf', 'svc__gamma': [1, 2]}])),
])
def test_build_param_grid(estimator, param_grid):
    assert build_param_grid(estimator) == param_grid


def test_build_param_grid_set_estimator():
    clf1 = SVC()
    clf2 = SVC()
    clf3 = LogisticRegression()
    clf4 = SGDClassifier()
    estimator = set_grid(Pipeline([('sel', set_grid(SelectKBest(), k=[1,2])),
                                   ('clf', None)]),
                         clf=[set_grid(clf1, kernel=['linear']),
                              clf3,
                              set_grid(clf2, kernel=['rbf'], gamma=[1, 2]),
                              clf4])
    param_grid = [{'clf': [clf1], 'clf__kernel': ['linear'], 'sel__k': [1, 2]},
                  {'clf': [clf2], 'clf__kernel': ['rbf'],
                   'clf__gamma': [1, 2], 'sel__k': [1, 2]},
                  {'clf': [clf3, clf4], 'sel__k': [1, 2]}]
    assert build_param_grid(estimator) == param_grid