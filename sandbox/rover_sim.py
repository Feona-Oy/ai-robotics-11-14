"""
rover_sim.py  --  Lunar rover sandbox

WHY THIS EXISTS
---------------
There is one real rover and many of you. Rover time is booked, limited,
and unforgiving: if you drive into a crater, nobody can walk over and
pick it up.

So you practise here. This sandbox behaves like the real rover, including
the annoying parts: the motors drift, the sensors are noisy, and the
craters are fatal. When your mission runs clean here, you book a slot and
fly it for real.

This is not a toy version of the job. It IS the job. NASA does not
joystick rovers on Mars. They rehearse, validate, then send the sequence.

HOW TO USE
----------
    rover = Rover()
    rover.forward(3)
    rover.turn_right(90)
    print(rover.read_colour())
    rover.show()
    rover.mission_report()

IMPORTANT: once you have seen the real lab platform, rename the methods
below to match its API exactly. Then the code you test here can be pasted
straight across with no changes. That is the whole point.
"""

import math
import random

# ---------------------------------------------------------------------
# The track. Edit it, break it, design your own.
#   '#'  navigation line
#   '.'  regolith (open ground)
#   'X'  crater  -- mission over
#   'R' 'G' 'B'  colour markers (samples to collect)
# ---------------------------------------------------------------------
TRACK = [
    "..........................",
    "..####################....",
    "..#..................#....",
    "..#..XXX......R......#....",
    "..#..XXX.............#....",
    "..#.............G....#....",
    "..#..................#....",
    "..####################....",
    "..........................",
]


class Rover:
    """A small, unreliable robot on the Moon."""

    def __init__(self, x=3.5, y=2.5, heading=0.0,
                 drift=1.5, sensor_noise=0.04, track=None):
        self.x = x                      # column position
        self.y = y                      # row position (increases downward)
        self.heading = heading          # degrees, 0 = east, clockwise
        self.drift = drift              # motor error, degrees per turn
        self.sensor_noise = sensor_noise
        self.track = track or TRACK
        self.log = []
        self.alive = True
        self.samples = []

    # -- internals ----------------------------------------------------

    def _cell_at(self, x, y):
        col, row = int(math.floor(x + 0.5)), int(math.floor(y + 0.5))
        if row < 0 or row >= len(self.track):
            return None
        line = self.track[row]
        if col < 0 or col >= len(line):
            return None
        return line[col]

    def _check_alive(self):
        cell = self._cell_at(self.x, self.y)
        if cell is None or cell == "X":
            self.alive = False
            self.log.append("*** MISSION LOST ***")
        return self.alive

    def _require_alive(self):
        if not self.alive:
            raise RuntimeError(
                "The rover is lost. Nobody is coming to get it. "
                "Restart the mission."
            )

    # -- movement -----------------------------------------------------

    def forward(self, cells):
        """Drive forward. One cell is roughly one rover length."""
        self._require_alive()
        steps = max(1, int(abs(cells) * 4))     # move in small increments
        for _ in range(steps):
            rad = math.radians(self.heading)
            self.x += (cells / steps) * math.cos(rad)
            self.y += (cells / steps) * math.sin(rad)
            if not self._check_alive():
                return
        self.heading += random.uniform(-self.drift, self.drift)
        self.log.append(f"forward({cells})  -> ({self.x:.2f}, {self.y:.2f})")

    def backward(self, cells):
        self.forward(-cells)

    def turn_right(self, degrees):
        self._require_alive()
        self.heading += degrees + random.uniform(-self.drift, self.drift)
        self.log.append(f"turn_right({degrees})  -> heading {self.heading:.1f}")

    def turn_left(self, degrees):
        self.turn_right(-degrees)

    # -- sensors ------------------------------------------------------

    def read_line(self):
        """Three line sensors: [left, centre, right]. 1 = on the line."""
        self._require_alive()
        readings = []
        for offset in (-0.35, 0.0, 0.35):
            ahead = math.radians(self.heading)
            side = math.radians(self.heading + 90)
            sx = self.x + 0.5 * math.cos(ahead) + offset * math.cos(side)
            sy = self.y + 0.5 * math.sin(ahead) + offset * math.sin(side)
            value = 1 if self._cell_at(sx, sy) == "#" else 0
            if random.random() < self.sensor_noise:     # sensors lie sometimes
                value = 1 - value
            readings.append(value)
        return readings

    def read_colour(self):
        """Colour marker under the rover, or 'none'."""
        self._require_alive()
        cell = self._cell_at(self.x, self.y)
        colours = {"R": "red", "G": "green", "B": "blue"}
        return colours.get(cell, "none")

    def collect_sample(self):
        colour = self.read_colour()
        if colour == "none":
            self.log.append("collect_sample()  -> nothing here")
            return False
        self.samples.append(colour)
        self.log.append(f"collect_sample()  -> {colour}")
        return True

    # -- output -------------------------------------------------------

    def show(self):
        """Print the track with the rover on it."""
        arrows = ["→", "↘", "↓", "↙", "←", "↖", "↑", "↗"]
        idx = int(((self.heading % 360) + 22.5) // 45) % 8
        marker = arrows[idx] if self.alive else "!"
        rc = int(math.floor(self.x + 0.5))
        rr = int(math.floor(self.y + 0.5))
        for r, line in enumerate(self.track):
            if r == rr and 0 <= rc < len(line):
                print(line[:rc] + marker + line[rc + 1:])
            else:
                print(line)
        print(f"pos ({self.x:.2f}, {self.y:.2f})  heading {self.heading:.1f}"
              f"  samples {self.samples}")

    def mission_report(self):
        print("=" * 46)
        print("MISSION REPORT")
        print("=" * 46)
        for entry in self.log:
            print(" ", entry)
        print("-" * 46)
        print(f"  status:  {'OPERATIONAL' if self.alive else 'LOST'}")
        print(f"  samples: {self.samples or 'none'}")
        print("=" * 46)


# ---------------------------------------------------------------------
# Demo mission. Delete this and write your own.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    rover = Rover(x=4, y=2, heading=0)

    # Mission: collect the red sample, then the green one.
    rover.forward(10)          # east along the top
    rover.turn_right(90)       # face south
    rover.forward(1)           # should be sitting on RED
    rover.collect_sample()

    rover.turn_left(90)        # face east
    rover.forward(2)
    rover.turn_right(90)       # face south
    rover.forward(2)           # should be sitting on GREEN
    rover.collect_sample()

    rover.show()
    rover.mission_report()
