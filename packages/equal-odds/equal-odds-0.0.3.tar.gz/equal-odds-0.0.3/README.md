# equal-odds
> This repository is under construction :construction:

![badge for PyPI publishing status](https://github.com/AndreFCruz/equal-odds/actions/workflows/python-publish.yml/badge.svg)

A fast adjust

## Installing

Install package from [PyPI](https://pypi.org/project/equal-odds/):
```
pip install equal-odds
```

Or, for development, you can clone the repo and install from local sources:
```
git clone https://github.com/AndreFCruz/equal-odds.git
pip install ./equal-odds
```

## Getting started

```py
# Given any trained model that outputs real-valued scores
fair_clf = RelaxedEqualOdds(
    predictor=lambda X: model.predict_proba(X)[:, -1],   # for sklearn API
    # predictor=model,  # use this for a callable model
    tolerance=0.05,     # fairness constraint tolerance
)

# Fit the fairness adjustment on some data
# This will find the optimal _fair classifier_
fair_clf.fit(X=X, y=y, group=group)

# Now you can use `fair_clf` as any other classifier
# You have to provide group information to compute fair predictions
y_pred_test = fair_clf(X=X_test, group=group_test)
```
