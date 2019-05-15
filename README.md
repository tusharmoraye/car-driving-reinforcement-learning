# Using Reinforcement Learning To Train An Autonomous Vehicle To Learn Driving

This is a project I created to learn the basics of reinforcement learning. It uses Python3, Pygame, Keras. It uses Q-learning (unsupervised) algorithm to learn how to drive itself without running into obstacles.


## Getting Started

### Quick Play

For those who wants to see car driving itself in action, I have included one trained model in `saved-models` folder and the playing.py is configured to load that model so just run the following command.

```
python3 playing.py
```

To train your own model follow the following procedure.

### Training

First, you need to train a model. This will save weights to the `saved-models` folder. *You may need to create this folder before running*. You can train the model by running:

```
python3 learning.py
```

It can take anywhere from an hour to 36 hours to train a model, depending on the complexity of the network and the size of your sample. However, it will spit out weights every 25,000 frames, so you can move on to the next step in much less time.

### Playing

Edit the `playing.py` file to change the path name for the model you want to load. 

Then, watch the car drive itself around the obstacles!

```
python3 playing.py
```

That's all there is to it.

### Plotting

Once you have a bunch of CSV files created via the learning, you can convert those into graphs by running:

```
python3 plotting.py
```

This will also spit out a bunch of loss and distance averages at the different parameters.

## Credits

I'm grateful to the following people and the work they did that helped me learn how to do this:

- A great tutorial on reinforcement learning : https://medium.com/@harvitronix/using-reinforcement-learning-in-python-to-teach-a-virtual-car-to-avoid-obstacles-6e782cc7d4c6

- Game used in this project : https://github.com/xpd54/Car-race-game


