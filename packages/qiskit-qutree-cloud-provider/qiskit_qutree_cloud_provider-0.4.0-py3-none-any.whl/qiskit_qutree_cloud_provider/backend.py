from qiskit.providers import BackendV2 as Backend
from qiskit.transpiler import Target
from qiskit.providers import Options
from qiskit.circuit.parameter import Parameter
from qiskit.circuit.library import (
    HGate,
    XGate,
    YGate,
    ZGate,
    SGate,
    SdgGate,
    IGate,
    UGate,
    CXGate,
    CZGate,
)
from qiskit.circuit.measure import Measure
from qiskit.result import Result
import grpc
import numpy as np

from .job import SyncJob
from .rpc import qutree_pb2, qutree_pb2_grpc
from .portfolio import (
    PortfolioParam,
    SCFParam,
    PortfolioConstraintParam,
    DiscreteSolverParam,
)
from ._version import __version__

from contextlib import contextmanager
import warnings
from abc import ABCMeta, abstractmethod


class QuTreeBackend(Backend, metaclass=ABCMeta):

    MAX_NQUBITS = 128

    def __init__(self, name="QuTreeBackend"):
        super().__init__(name=name, backend_version=__version__)

        self._target = Target(num_qubits=self.MAX_NQUBITS)
        theta, phi, lam = Parameter("θ"), Parameter("ϕ"), Parameter("λ")
        for _g in (
            HGate(),
            XGate(),
            YGate(),
            ZGate(),
            SGate(),
            SdgGate(),
            IGate(),
            UGate(theta, phi, lam),
            CXGate(),
            CZGate(),
            Measure(),
        ):
            self._target.add_instruction(_g)

        self.options.set_validator("shots", (1, 4096))
        self.options.set_validator("tree_type", ["binary", "train", "compact"])
        self.options.set_validator("tree_structure", str)
        self.options.set_validator("vbond_dim", (1, 2048))
        self.options.set_validator("vbond_dim_increment", (0, 256))

    @classmethod
    def _default_options(cls):
        return Options(
            shots=1024,
            tree_type="binary",
            tree_structure="",
            vbond_dim=32,
            vbond_dim_increment=0,
        )

    @property
    def target(self):
        return self._target

    @property
    def max_circuits(self):
        return None

    def _update_options(self, kwargs):
        _kwargs = {}
        for k, v in kwargs.items():
            if k not in self.options.__dict__:
                warnings.warn(
                    f"Option {k} is not used by this backend", UserWarning, stacklevel=2
                )
                continue
            _kwargs[k] = v
        self.options.update_options(**_kwargs)

    @abstractmethod
    def _run(self, circuits, **kwargs):
        """Circuit execution without the Qiskit job boilerplates"""
        pass

    def run(self, circuits, **kwargs):
        if type(circuits) not in (list, tuple):
            circuits = [circuits]
        rs = self._run(circuits, **kwargs)
        results = []
        time_stat = 0
        for r in rs:
            data = dict(
                counts=r.counts,
            )
            results.append(
                dict(
                    success=True,
                    shots=self.options.shots,
                    data=data,
                )
            )
            time_stat += r.time_taken
        job_id = ""
        result = Result.from_dict(
            dict(
                results=results,
                success=True,
                backend_name=self.name,
                backend_version=self.backend_version,
                job_id=job_id,
                qobj_id=", ".join(x.name for x in circuits),
                time_taken=time_stat / 1000,
            )
        )
        return SyncJob(self, job_id, result)

    @abstractmethod
    def compute_expectation(self, obs, circuit, **kwargs):
        """Compute <circuit|obs|circuit>
        Internal interface for ``QuTreeEstimator``.
        """
        pass

    @abstractmethod
    def _run_portfolio_optimization(
        self,
        portfolio_param: PortfolioParam,
        scf_param: SCFParam,
        **kwargs,
    ):
        pass

    # fmt: off
    def run_portfolio_optimization(self,
        mu, covariance, alpha, gamma, rho, K,
        n_iter=5, n_krylov=10, n_itp=0, beta=2.0, seed=-1,
        **kwargs,
    ):
        """Run Portfolio optimization with SCF

        Hamiltonian:
            H = -alpha * mu * omega + gamma / 2 * omega^T * sigma * omega + rho * (u^T * omega - k)^2

        where
           alpha: return factor
           gamma: risk factor
           rho:   budget constraint factor
           k:     budget constraint
        """
        covariance = np.ravel(covariance)
        _r = self._run_portfolio_optimization(
            PortfolioParam(mu, covariance, alpha, gamma, rho, K),
            SCFParam(n_iter, n_krylov, n_itp, beta, seed),
            **kwargs,
        )
        return self._scf_result(_r)
    # fmt: on

    @abstractmethod
    def _run_portfolio_optimization_discrete(
        self,
        portfolio_param: PortfolioConstraintParam,
        solver_param: DiscreteSolverParam,
        **kwargs,
    ):
        pass

    # fmt: off
    def run_portfolio_optimization_discrete(self,
        mu, covariance, alpha, gamma, a, b, r,
        n_sweep=10, seed=-1,
        **kwargs,
    ):
        """Run Portfolio optimization with SCF (discrete solver)

        Hamiltonian:
            H = -alpha * mu * omega + gamma / 2 * omega^T * sigma * omega
        with constraints:
            a * omega <= b;
            omega^T * sigma * omega <= r^2

        where
           alpha: return factor
           gamma: risk factor
           a, b:  budget constraints
           r:     risk constraint
        """
        covariance = np.ravel(covariance)
        if np.isinf(r):
            r = np.finfo(np.float32).max ** 0.5 # protobuf does not support inf
        _r = self._run_portfolio_optimization_discrete(
            PortfolioConstraintParam(mu, covariance, alpha, gamma, a, b, r),
            DiscreteSolverParam(n_sweep, seed),
            **kwargs,
        )
        return self._scf_result(_r)
    # fmt: on

    def _scf_result(self, r):
        job_id = ""
        result0 = dict(
            success=True, shots=self.options.shots, data=dict(counts=r.counts)
        )
        result = Result.from_dict(
            dict(
                results=[result0],
                success=True,
                backend_name=self.name,
                backend_version=self.backend_version,
                job_id=job_id,
                qobj_id="",
                time_taken=r.time_taken / 1000,
            )
        )
        return SyncJob(self, job_id, result)


class QuTreeCloudBackend(QuTreeBackend):
    def __init__(self, addr):
        super().__init__(name="QuTreeCloudBackend")
        self.addr = addr

    @contextmanager
    def _connect(self):
        grpc_chan = (
            grpc.secure_channel(self.addr, grpc.ssl_channel_credentials())
            if self.addr.endswith(":443")
            else grpc.insecure_channel(self.addr)
        )
        with grpc_chan as channel:
            yield qutree_pb2_grpc.QuTreeRunnerStub(channel)

    def _run(self, circuits, **kwargs):
        self._update_options(kwargs)
        with self._connect() as stub:
            response = stub.RunCircuit(
                qutree_pb2.CircuitsWithOptions(
                    circuits=[circuit_pack(c) for c in circuits],
                    options=qutree_pb2.Options(**self.options.__dict__),
                )
            )
        return response.results

    def compute_expectation(self, obs, circuit, **kwargs):
        self._update_options(kwargs)
        with self._connect() as stub:
            response = stub.ComputeExpectation(
                qutree_pb2.CircuitsObservablesWithOptions(
                    circuits=[circuit_pack(circuit)],
                    observables=[pauli_pack(obs)],
                    options=qutree_pb2.Options(**self.options.__dict__),
                )
            )
        return response.results[0]

    def _run_portfolio_optimization(
        self,
        portfolio_param: PortfolioParam,
        scf_param: SCFParam,
        **kwargs,
    ):
        self._update_options(kwargs)
        with self._connect() as stub:
            response = stub.RunPortfolioOptimization(
                qutree_pb2.PortfolioSCFParamWithOptions(
                    portfolio_param=qutree_pb2.PortfolioParam(
                        **portfolio_param.__dict__
                    ),
                    scf_param=qutree_pb2.SCFParam(**scf_param.__dict__),
                    options=qutree_pb2.Options(**self.options.__dict__),
                )
            )
        return response

    def _run_portfolio_optimization_discrete(
        self,
        portfolio_param: PortfolioConstraintParam,
        solver_param: DiscreteSolverParam,
        **kwargs,
    ):
        self._update_options(kwargs)
        with self._connect() as stub:
            response = stub.RunPortfolioOptimizationDiscrete(
                qutree_pb2.PortfolioDiscreteSolverParamWithOptions(
                    portfolio_constraint_param=qutree_pb2.PortfolioConstraintParam(
                        **portfolio_param.__dict__
                    ),
                    discrete_solver_param=qutree_pb2.DiscreteSolverParam(**solver_param.__dict__),
                    options=qutree_pb2.Options(**self.options.__dict__),
                )
            )
        return response


def circuit_encode(circuit):
    for op in circuit:
        if op.operation.name == "barrier":  # FIXME
            continue
        yield (
            op.operation.name,
            [circuit.find_bit(q).index for q in op.qubits],
            op.operation.params,
        )


def circuit_pack(circuit):
    return qutree_pb2.Circuit(
        ops=[
            qutree_pb2.Operation(name=name, qubits=qubits, params=params)
            for name, qubits, params in circuit_encode(circuit)
        ],
        nqubit=circuit.num_qubits,
    )


def pauli_encode(obs):
    for pauli, coeff in zip(obs.paulis, np.real(obs.coeffs)):
        yield (
            coeff,
            np.nonzero(pauli.z)[0],
            np.nonzero(pauli.x)[0],
        )


def pauli_pack(obs):
    return qutree_pb2.Observable(
        paulis=[
            qutree_pb2.PauliOp(coeff=coeff, ind_z=ind_z, ind_x=ind_x)
            for coeff, ind_z, ind_x in pauli_encode(obs)
        ],
    )
