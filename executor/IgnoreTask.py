from executor.ITask import ITask


class IgnoreTask(ITask):
    def __init__(self, task):
        self.task = task

    def run(self, countdown: int = 0):
        pass

    def persist(self, todb: bool = False):
        pass
    