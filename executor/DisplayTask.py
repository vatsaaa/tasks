from executor.ITask import ITask


class DisplayTask(ITask):
    def __init__(self, task):
        self.task = task

    def run(self):
        ## TODO: Send message to UI that new data is ready to for display
        print(self.task)