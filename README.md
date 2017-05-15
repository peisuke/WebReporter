# WebReporter

WebReporter is a browser based traning curves visualizer, which is extention for chainer. This extention uses [HyperBoard](https://github.com/WarBean/hyperboard.git). It helps you to train on a remote server and visualize training curves on the local browser in real-time. 

## Installation

At first, it is nessesary to install [HyperBoard](https://github.com/WarBean/hyperboard.git). See the [link](https://github.com/WarBean/hyperboard/blob/463d1be007ad8b29de47765684d126efb47fb61a/README.md).

Screenshot:

<img src="https://github.com/peisuke/WebReporter/blob/master/screenshot.jpg" width="400">

## How to use

This is an LogReport extension of chainer. To use this extension, add to Trainer in the same manner as another reporter. Usage is shown below. 

class WebReport(hyperparameters, metric2scale, criteria2metric, log_report='LogReport', username='', password='', address= '127.0.0.1', port=5000)

- hyperparameters - Conditions in the board.
- metric2scale - Relative scales to plot the board.
- criteria2metric - Keys of values to show.
- log_report - LogReporter.
- username - User name parameter for reporting to HyperBoard
- password - Password parameter for reporting to HyperBoard
- address - IP Address the HyperBoard is working on.

### Example

```py
hyperparameters = {'batchsize':args.batchsize, 'unit':args.unit}
metric2scale = {'loss' : 1.0, 'accuracy' : 1.0}
criteria2metric = {
    'main/loss' : 'loss', 
    'validation/main/loss' : 'loss',
    'main/accuracy' : 'accuracy', 
    'validation/main/accuracy' : 'accuracy'
}
trainer.extend(WebReport(hyperparameters, metric2scale, criteria2metric))
````
