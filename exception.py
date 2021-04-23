from configurator import s
from task import TASKS


class TaskNotFoundError(Exception):
    def __init__(self, task):
        self.task = task

    def __str__(self):
        return f"{self.task} not in {TASKS.keys()}"


class TaskRunningError(Exception):
    def __str__(self):
        return s.error_task_running


class DeviceError(Exception):
    pass


class ReasonRunOutException(Exception):
    def __str__(self):
        return s.error_reason_run_out