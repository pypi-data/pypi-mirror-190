import logging
from typing import Any, Dict, List, Optional, Tuple

from ert._c_wrappers.enkf import RunContext
from ert._c_wrappers.enkf.enkf_main import EnKFMain, QueueConfig
from ert._c_wrappers.enkf.enums import HookRuntime, RealizationStateEnum
from ert.analysis import ErtAnalysisError
from ert.ensemble_evaluator import EvaluatorServerConfig
from ert.shared.models import BaseRunModel, ErtRunError

logger = logging.getLogger(__file__)
experiment_logger = logging.getLogger("ert.experiment_server.ensemble_experiment")


class MultipleDataAssimilation(BaseRunModel):
    """
    Run multiple data assimilation (MDA) ensemble smoother with custom weights.
    """

    default_weights = "4, 2, 1"

    def __init__(
        self,
        simulation_arguments: Dict[str, Any],
        ert: EnKFMain,
        queue_config: QueueConfig,
        id_: str,
    ):
        super().__init__(simulation_arguments, ert, queue_config, id_, phase_count=2)
        self.weights = MultipleDataAssimilation.default_weights

    def setAnalysisModule(self, module_name: str) -> None:
        module_load_success = self.ert().analysisConfig().select_module(module_name)

        if not module_load_success:
            raise ErtRunError(f"Unable to load analysis module '{module_name}'!")

    def runSimulations(
        self, evaluator_server_config: EvaluatorServerConfig
    ) -> RunContext:
        self._checkMinimumActiveRealizations(
            self._simulation_arguments["active_realizations"].count(True)
        )
        weights = self.parseWeights(self._simulation_arguments["weights"])
        iteration_count = len(weights)

        self.setAnalysisModule(self._simulation_arguments["analysis_module"])

        logger.info(
            f"Running MDA ES for {iteration_count}  "
            f'iterations\t{", ".join(str(weight) for weight in weights)}'
        )
        weights = self.normalizeWeights(weights)

        weight_string = ", ".join(str(round(weight, 3)) for weight in weights)
        logger.info(f"Running MDA ES on (weights normalized)\t{weight_string}")

        self.setPhaseCount(iteration_count + 1)  # weights + post
        phase_string = (
            f"Running MDA ES {iteration_count} "
            f'iteration{"s" if (iteration_count != 1) else ""}.'
        )
        self.setPhaseName(phase_string, indeterminate=True)

        update_id = None
        enumerated_weights = list(enumerate(weights))
        starting_iteration = self._simulation_arguments["start_iteration"]
        case_format = self._simulation_arguments["target_case"]
        storage_manager = self.ert().storage_manager
        if starting_iteration > 0:
            if case_format % starting_iteration not in storage_manager:
                raise ErtRunError(
                    f"Source case {case_format % starting_iteration} for iteration "
                    f"{starting_iteration} does not exists in {storage_manager.cases}."
                    " If you are attempting to restart ESMDA from a iteration other "
                    "than 0, make sure the target case format is the same as for the "
                    f"original run.(Current target case format: {case_format})"
                )
        else:
            prior_fs = storage_manager.add_case(case_format % starting_iteration)
            active_realizations = [
                i
                for i, val in enumerate(
                    self._simulation_arguments["active_realizations"]
                )
                if val
            ]
            self.ert().sample_prior(prior_fs, active_realizations)

        weights_to_run = enumerated_weights[min(starting_iteration, len(weights)) :]

        for iteration, weight in weights_to_run:
            is_first_iteration = iteration == 0
            if is_first_iteration:
                mask = self._simulation_arguments["active_realizations"]
            else:
                mask = None
            run_context = self.create_context(iteration, mask=mask)
            _, ensemble_id = self._simulateAndPostProcess(
                run_context, evaluator_server_config, update_id=update_id
            )
            if is_first_iteration:
                self.ert().runWorkflows(HookRuntime.PRE_FIRST_UPDATE)
            self.ert().runWorkflows(HookRuntime.PRE_UPDATE)
            update_id = self.update(
                run_context=run_context, weight=weight, ensemble_id=ensemble_id
            )
            self.ert().runWorkflows(HookRuntime.POST_UPDATE)

        self.setPhaseName("Post processing...", indeterminate=True)
        run_context = self.create_context(len(weights), update=False)
        self._simulateAndPostProcess(
            run_context, evaluator_server_config, update_id=update_id
        )

        self.setPhase(iteration_count + 1, "Simulations completed.")

        return run_context

    def _count_active_realizations(self, run_context: RunContext) -> int:
        return sum(run_context.mask)

    def update(self, run_context: RunContext, weight: float, ensemble_id: str) -> str:
        next_iteration = run_context.iteration + 1

        phase_string = f"Analyzing iteration: {next_iteration} with weight {weight}"
        self.setPhase(self.currentPhase() + 1, phase_string, indeterminate=True)

        self.facade.set_global_std_scaling(weight)
        try:
            self.facade.smoother_update(run_context)
        except ErtAnalysisError as e:
            raise ErtRunError(
                "Analysis of simulation failed for iteration:"
                f"{next_iteration}. The following error occured {e}"
            ) from e
        # Push update data to new storage
        analysis_module_name = self.ert().analysisConfig().active_module_name()
        update_id = self._post_update_data(
            parent_ensemble_id=ensemble_id, algorithm=analysis_module_name
        )

        return update_id

    def _simulateAndPostProcess(
        self,
        run_context: RunContext,
        evaluator_server_config: EvaluatorServerConfig,
        update_id: Optional[str] = None,
    ) -> Tuple[int, str]:
        iteration = run_context.iteration

        phase_string = f"Running simulation for iteration: {iteration}"
        self.setPhaseName(phase_string, indeterminate=True)
        self.ert().createRunPath(run_context)

        phase_string = f"Pre processing for iteration: {iteration}"
        self.setPhaseName(phase_string)
        self.ert().runWorkflows(HookRuntime.PRE_SIMULATION)

        # Push ensemble, parameters, observations to new storage
        new_ensemble_id = self._post_ensemble_data(update_id=update_id)

        phase_string = f"Running forecast for iteration: {iteration}"
        self.setPhaseName(phase_string, indeterminate=False)

        num_successful_realizations = self.run_ensemble_evaluator(
            run_context, evaluator_server_config
        )

        # Push simulation results to storage
        self._post_ensemble_results(new_ensemble_id)

        num_successful_realizations += self._simulation_arguments.get(
            "prev_successful_realizations", 0
        )
        self.checkHaveSufficientRealizations(num_successful_realizations)

        phase_string = f"Post processing for iteration: {iteration}"
        self.setPhaseName(phase_string, indeterminate=True)
        self.ert().runWorkflows(HookRuntime.POST_SIMULATION)

        return num_successful_realizations, new_ensemble_id

    @staticmethod
    def normalizeWeights(weights: List[float]) -> List[float]:
        """Scale weights such that their reciprocals sum to 1.0,
        i.e., sum(1.0 / x for x in weights) == 1.0.
        See for example Equation 38 of evensen2018 - Analysis of iterative
        ensemble smoothers for solving inverse problems.
        """
        if not weights:
            return []
        weights = [weight for weight in weights if abs(weight) != 0.0]

        length = sum(1.0 / x for x in weights)
        return [x * length for x in weights]

    @staticmethod
    def parseWeights(weights: str) -> List:
        if not weights:
            return []

        elements = weights.split(",")
        elements = [
            element.strip() for element in elements if not element.strip() == ""
        ]

        result = []
        for element in elements:
            try:
                f = float(element)
                if f == 0:
                    logger.info("Warning: 0 weight, will ignore")
                else:
                    result.append(f)
            except ValueError:
                raise ValueError(f"Warning: cannot parse weight {element}")

        return result

    def create_context(
        self,
        itr: int,
        mask: Optional[List[bool]] = None,
        update: bool = True,
    ) -> RunContext:
        target_case_format = self._simulation_arguments["target_case"]
        fs_manager = self.ert().storage_manager

        source_case_name = target_case_format % itr
        sim_fs = fs_manager[source_case_name]
        if update:
            target_fs = fs_manager.add_case(target_case_format % (itr + 1))
        else:
            target_fs = None

        if mask is None:
            initialized_and_has_data: RealizationStateEnum = (
                RealizationStateEnum.STATE_HAS_DATA  # type: ignore
                | RealizationStateEnum.STATE_INITIALIZED
            )
            mask = sim_fs.getStateMap().createMask(initialized_and_has_data)
            # Make sure to only run the realizations which was passed in as argument
            for idx, (valid_state, run_realization) in enumerate(
                zip(mask, self._initial_realizations_mask)
            ):
                mask[idx] = valid_state and run_realization

        run_context = self.ert().create_ensemble_smoother_run_context(
            source_filesystem=sim_fs,
            target_filesystem=target_fs,
            active_mask=mask,
            iteration=itr,
        )
        self._run_context = run_context
        self._last_run_iteration = run_context.iteration
        self.ert().getEnkfFsManager().switchFileSystem(sim_fs.case_name)
        return run_context

    @classmethod
    def name(cls) -> str:
        return "Multiple Data Assimilation (ES MDA) - Recommended"
