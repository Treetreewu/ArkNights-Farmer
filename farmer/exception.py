from farmer.configurator import s


class TaskNotFoundError(Exception):
    def __init__(self, task):
        self.task = task

    def __str__(self):
        return f"task {self.task} not found"


class TaskRunningError(Exception):
    def __str__(self):
        return s.error_task_running


class DeviceError(Exception):
    pass


class ReasonRunOutException(Exception):
    def __str__(self):
        return s.error_reason_run_out