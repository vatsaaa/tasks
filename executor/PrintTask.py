from executor.ITask import ITask


class PrintTask():
    def __init__(self, data):
        super().__init__()
        self._data = data

    def run(self, countdown: int = 0):
        super().run()
        print(self._data)

    def persist(self, todb: bool = False):
        super().persist(todb=todb)
        print("Check")

