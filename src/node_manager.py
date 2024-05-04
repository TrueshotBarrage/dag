from time import sleep, time
from threading import Thread

def pp(fstr, start_time=None):
    time_append = f"[{(time() - start_time).__format__('g')}] " if start_time else ""
    print(f"{time_append}{fstr}")

class Task():
    def __init__(self, priority=""):
        self.priority = priority
        self.timer = self._init_timer(priority)
    
    def _init_timer(self, prio):
        if prio == "":
            return 3
        else:
            return ord(prio) - ord("A") + 1
    
    def __repr__(self) -> str:
        return f"""Task<priority:{self.priority},timer:{self.timer}>"""

class TaskManager():
    def __init__(self, graph):
        self.graph = graph
        self.ex_order = self.graph.topsort()

        self.queue = []

    def _add_job(self):
        start = time()
        for n in self.ex_order:
            task = Task(n)
            self.queue.append(task)
            pp(f"[+]: {task} => Queue: {self.queue}", start)
            sleep(0.2)
    
    def _run_job(self, runtime=None):
        run_for = runtime if runtime else 100000
        start = time()

        # Slow start...
        pp(f"Worker starting in 5 seconds!", start)
        sleep(5)

        while time() - start <= run_for:
            try:
                task = self.queue.pop(0)
                pp(f"[-]: {task}...", start)
                sleep(task.timer)
                pp(f"Worker free => Queue: {self.queue}", start)
            except IndexError:
                sleep(1)
        
    def execute(self):
        # Add items to the queue from the graph's topological sort
        t0 = Thread(target=self._add_job)
        t0.start()

        # Begin execution of the nodes by assigning tasks to the worker 
        t1 = Thread(target=self._run_job, kwargs={"runtime": 30})
        t1.start()