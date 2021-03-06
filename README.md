# reversi-bot

Currently, this project is only compatible with Linux. Apologies to anyone else who is interested 
(though you can probably make it work since Python is cross platform).

This is an attempt to implement simple Artificial Neural Networks to play the game of Reversi (also called Othello). 
Please notify me is you find any of my plethora of mistakes... 

NOTE: The Reversi playing engine 'Edax' engine is bundled with this repository and I do not possess any rights to that 
engine. See bottom for more information.

## Getting Started

If you don't know how to play Reversi, look [here](https://en.wikipedia.org/wiki/Reversi#Rules).

### Dependencies

This project is built on Python 2.7. Please install Python before continuing.
```bash
# on Debian/Ubuntu
sudo apt-get install python
```

A few additional modules were used to build this project (all under python):
  - anytree
  - Cython
  - numpy
  - matplotlib (optional)

Installation should be easy if you have python installed:
```bash
pip install anytree
pip install cython
pip install numpy
pip install matplotlib
```

### Installing

Clone the directory:

```bash
git clone https://github.com/steven-xia/ReversiBot
```

Then compile the necessary components:
```bash
python setup.py build_ext --inplace
```

If all the dependencies are met, you can easily run with (inside the folder). 

```bash
python gui.py
```

If you want to train, you need to unzip the training data file: 'training_data.zip':
```
unzip training_data.zip
```
### Other notes

Data collection is done with the following command. The number of threads can be set in `edax_wrapper.py` under the 
variable `THREADS`.

```bash
python collect_data.py
```

Training is done with the `train.py` file. Any configurations to the network architecture should be done by changing
the 'constants' found at the top the file. Training can be done with the command:

```bash
python train.py
```

## Acknowledgments

* [Edax](https://github.com/abulmo/edax-reversi) -- released under GNU GPL version 3
