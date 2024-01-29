import multiprocessing
import traceback


class XtProcess(multiprocessing.Process):
    def __init__(self, *args, **kwargs) -> None:
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = multiprocessing.Pipe()
        self._exception = None

    def run(self):
        try:
            multiprocessing.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()  # noqa: F821
            self._cconn.send((e, tb))
            raise e

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception
