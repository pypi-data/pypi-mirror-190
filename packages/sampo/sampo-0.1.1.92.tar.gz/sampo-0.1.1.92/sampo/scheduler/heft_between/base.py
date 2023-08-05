from typing import List, Optional, Dict, Iterable

from sampo.metrics.resources_in_time.base import ResourceOptimizer
from sampo.scheduler.base import SchedulerType
from sampo.scheduler.heft.base import HEFTScheduler
from sampo.scheduler.heft.time_computaion import calculate_working_time_cascade
from sampo.scheduler.resource.coordinate_descent import CoordinateDescentResourceOptimizer
from sampo.scheduler.timeline.base import Timeline
from sampo.scheduler.timeline.momentum_timeline import MomentumTimeline
from sampo.scheduler.utils.multi_contractor import get_worker_borders, run_contractor_search
from sampo.schemas.contractor import Contractor, get_worker_contractor_pool
from sampo.schemas.graph import GraphNode
from sampo.schemas.resources import Worker
from sampo.schemas.schedule_spec import ScheduleSpec
from sampo.schemas.scheduled_work import ScheduledWork
from sampo.schemas.time import Time
from sampo.schemas.time_estimator import WorkTimeEstimator
from sampo.utilities.base_opt import dichotomy_int


class HEFTBetweenScheduler(HEFTScheduler):

    def __init__(self,
                 scheduler_type: SchedulerType = SchedulerType.HEFTAddBetween,
                 resource_optimizer: ResourceOptimizer = CoordinateDescentResourceOptimizer(dichotomy_int),
                 work_estimator: Optional[WorkTimeEstimator or None] = None):
        super().__init__(scheduler_type, resource_optimizer, work_estimator)

    def build_scheduler(self, ordered_nodes: List[GraphNode],
                        contractors: List[Contractor],
                        spec: ScheduleSpec,
                        work_estimator: WorkTimeEstimator = None,
                        assigned_parent_time: Time = Time(0),
                        timeline: Timeline | None = None) \
            -> tuple[Iterable[ScheduledWork], Time, MomentumTimeline]:
        """
        Find optimal number of workers who ensure the nearest finish time.
        Finish time is combination of two dependencies: max finish time, max time of waiting of needed workers
        This is selected by iteration from minimum possible numbers of workers until then the finish time is decreasing

        :param ordered_nodes:
        :param contractors:
        :param spec: spec for current scheduling
        :param timeline: the previous used timeline can be specified to handle previously scheduled works
        :param assigned_parent_time: start time of the whole schedule(time shift)
        :param work_estimator:
        :return:
        """
        worker_pool = get_worker_contractor_pool(contractors)
        # dict for writing parameters of completed_jobs
        node2swork: Dict[GraphNode, ScheduledWork] = {}
        # list for support the queue of workers
        if not isinstance(timeline, MomentumTimeline):
            timeline = MomentumTimeline(ordered_nodes, contractors)

        for index, node in enumerate(reversed(ordered_nodes)):  # the tasks with the highest rank will be done first
            work_unit = node.work_unit
            work_spec = spec.get_work_spec(work_unit.id)
            if node in node2swork:  # here
                continue

            def run_with_contractor(contractor: Contractor) -> tuple[Time, Time, List[Worker]]:
                min_count_worker_team, max_count_worker_team, workers \
                    = get_worker_borders(worker_pool, contractor, work_unit.worker_reqs)

                if len(workers) != len(work_unit.worker_reqs):
                    return Time(0), Time.inf(), []

                worker_team = [worker.copy() for worker in workers]

                def get_finish_time(cur_worker_team):
                    return timeline.find_min_start_time(node, cur_worker_team, node2swork,
                                                        assigned_parent_time, work_estimator) \
                           + calculate_working_time_cascade(node, cur_worker_team, work_estimator)

                # apply worker team spec
                self.optimize_resources_using_spec(work_unit, worker_team, work_spec,
                                                   lambda optimize_array: self.resource_optimizer.optimize_resources(
                                                       worker_pool, worker_team,
                                                       optimize_array,
                                                       min_count_worker_team, max_count_worker_team,
                                                       get_finish_time))

                c_st = None
                if index == 0:  # we are scheduling the work `start of the project`
                    c_st = assigned_parent_time  # this work should always have st = 0, so we just re-assign it

                c_st, _, exec_times = \
                    timeline.find_min_start_time_with_additional(node, worker_team, node2swork, c_st,
                                                                 assigned_parent_time, work_estimator)

                c_ft = c_st
                for node_lag, node_time in exec_times.values():
                    c_ft += node_lag + node_time

                return c_st, c_ft, worker_team

            st, ft, contractor, best_worker_team = run_contractor_search(contractors, run_with_contractor)

            # finish scheduling with time spec
            timeline.schedule(index, node, node2swork, best_worker_team, contractor,
                              st, work_spec.assigned_time, assigned_parent_time, work_estimator)

        # parallelize_local_sequence(ordered_nodes, 0, len(ordered_nodes), node2swork)
        # recalc_schedule(reversed(ordered_nodes), node2swork, agents, work_estimator)

        schedule_start_time = min([swork.start_time for swork in node2swork.values() if
                                   len(swork.work_unit.worker_reqs) != 0])

        return node2swork.values(), schedule_start_time, timeline
