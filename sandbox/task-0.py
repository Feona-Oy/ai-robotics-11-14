"""
TASK -- Session 1.

Your teacher just showed that with enough motor drift the rover
sometimes fails. But "sometimes" is not a result. An engineer needs
a number.

Run the mission 20 times at each drift level and count how many times
it worked. This is your first real experiment.

Put this file next to rover_sim.py and press Run.
"""

from rover_sim import Rover


def one_mission(drift):
    """A single run. Returns True if the sample was collected."""
    r = Rover(x=4, y=2, heading=0, drift=drift)
    try:
        for _ in range(10):
            r.forward(1)
        r.turn_right(90)
        r.forward(1)
        r.collect_sample()
    except RuntimeError:
        pass
    return bool(r.samples)


for drift in [0, 1.5, 5, 10]:
    successes = 0
    for attempt in range(20):
        if one_mission(drift):
            successes += 1
    print(f"drift {drift}:  {successes} out of 20 missions succeeded")


# WRITE THE RESULT IN YOUR NOTEBOOK, then answer:
#
# 1. Run the file again. Did you get the same numbers? Why not?
# 2. At what drift level does the rover stop being reliable?
# 3. What would you have to add to the program so that it still
#    works at drift 10?
#
# IF YOU FINISH EARLY:
# look at r.read_line() -- three line sensors.
# Try checking after each forward(1) where you have drifted to, and
# correcting the heading. If you get that working, you have just
# invented feedback control, and we are going to spend the next
# several sessions on it.
