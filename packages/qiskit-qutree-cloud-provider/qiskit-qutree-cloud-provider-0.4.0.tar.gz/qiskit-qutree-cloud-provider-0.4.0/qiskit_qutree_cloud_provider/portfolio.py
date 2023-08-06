"""Parameters used by Portfolio Optimization;
definitions should match with that of qutree.proto
"""
from attrs import define
from typing import List


@define(slots=False)
class PortfolioParam:
    mu: List[float]
    covariance: List[float]
    alpha: float
    gamma: float
    rho: float
    k: float


@define(slots=False)
class SCFParam:
    n_iter: int
    n_krylov: int
    n_itp: int
    beta: float
    seed: int


@define(slots=False)
class PortfolioConstraintParam:
    mu: List[float]
    covariance: List[float]
    alpha: float
    gamma: float
    a: list[float]
    b: list[float]
    r: float


@define(slots=False)
class DiscreteSolverParam:
    n_sweep: int
    seed: int
