
class Metric(object):
    def __init__(self):
        pass  # Don't know yet what we'll want to put in this

    def compute(self, predictions=None, references=None, **kwargs):
        """ This method defines the common API for all the metrics in the library """
        raise NotImplementedError