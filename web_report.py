import sys

from hyperboard import Agent

from chainer.training import extension
from chainer.training.extensions import log_report as log_report_module


class WebReport(extension.Extension):

    """Trainer extension to view the accumulated results on the web.

    This extension uses the hyperboard libraly by a :class:`LogReport` extension 
    to view specified entries of the log on the web.

    Args:
        entries (list of str): List of keys of observations to print.
        log_report (str or LogReport): Log report to accumulate the
            observations. This is either the name of a LogReport extensions
            registered to the trainer, or a LogReport instance to use
            internally.
        out: Stream to print the bar. Standard output is used by default.

    """

    def __init__(self, hyperparameters, metric2scale, criteria2metric, log_report='LogReport', username = '', password = '', address = '127.0.0.1', port = 5000):
        self._metric2scale = metric2scale
        self._criteria2metric = criteria2metric
        self._log_report = log_report
        self._agent = Agent(username, password, address, port)
      
        self._name_list = [] 
        self._criteria_list = []
        for criteria in self._criteria2metric.keys():
            metric = criteria2metric[criteria]
            hyperparameters['criteria'] = criteria
            print('register criteria <%s> as metric <%s>' % (criteria, metric))

            name = self._agent.register(hyperparameters, metric, overwrite = True)
            print(name)
            self._name_list.append(name)
            self._criteria_list.append(criteria)
           
        self._log_len = 0  # number of observations already printed

    def __call__(self, trainer):
        log_report = self._log_report
        if isinstance(log_report, str):
            log_report = trainer.get_extension(log_report)
        elif isinstance(log_report, log_report_module.LogReport):
            log_report(trainer)  # update the log report
        else:
            raise TypeError('log report has a wrong type %s' %
                            type(log_report))

        log = log_report.log
        log_len = self._log_len
        while len(log) > log_len:
            self._print(log_len, log[log_len])
            log_len += 1
        self._log_len = log_len

    def serialize(self, serializer):
        log_report = self._log_report
        if isinstance(log_report, log_report_module.LogReport):
            log_report.serialize(serializer['_log_report'])

    def _print(self, index, observation):
        for name, criteria in zip(self._name_list, self._criteria_list):
            metric = self._criteria2metric[criteria]
            scale = self._metric2scale[metric]
            value = observation[criteria]
            value *= scale
            self._agent.append(name, index, value)
