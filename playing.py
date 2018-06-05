"""
Once a model is learned, use this to play it.
"""

import cargame
import numpy as np
from nn import neural_net

NUM_SENSORS = 7


def play(model):

    car_distance = 0
    game_state = cargame.GameState()

    # Do nothing to get initial.
    _, state = game_state.frame_step((0))

    # Move.
    while True:
        car_distance += 1

        # Choose action.
        action = (np.argmax(model.predict(state, batch_size=1)))

        # Take action.
        _, state = game_state.frame_step(action)

        # Tell us something.
        if car_distance % 1000 == 0:
            print("Current distance: %d frames." % car_distance)


if __name__ == "__main__":
    saved_model = 'saved-models/128-128-64-50000-100000.h5'
    model = neural_net(NUM_SENSORS, [128, 128], saved_model)
    play(model)
