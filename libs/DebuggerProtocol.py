from abc import ABCMeta, abstractmethod
class DebuggerProtocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def step_in(self):
        pass

    @abstractmethod
    def cont_exec(self):
        pass

    @abstractmethod
    def step_out(self):
        pass

