# -*- coding: utf-8 -*-
"""Module helping with tree map solutions for Advent of Code 2020."""

from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np


class TreeMap:

    """A map of trees on a regular grid."""

    map: np.array
    _lastpath: Optional[List[Tuple]] = None

    def __init__(self, fpath):
        """Initialise map.

        :param fpath:  Path to file with base map for tree
        """
        self.load_map(fpath)

    def load_map(self, fpath):
        """Load base map for trees as numpy array

        :param fpath: Path to file with base map for tree

        The map repeats to the right.
        """
        maplist = []
        with Path(fpath).open("r") as ifh:
            for line in ifh.readlines():
                maplist.append(self.parse_line(line.strip()))
            ifh.seek(0)
            self.mapstr = ifh.read()

        self.map = np.array(maplist)

    def parse_line(self, data: str):
        """Return map line as list of [1,0] values.

        :param data:  line from base map

        We define trees (#) as 1 and spaces (.) as 0.
        """
        return [1 if _ == "#" else 0 for _ in data]

    def trees_in_line(self, right: int, down: int, start_x: int = 0, start_y: int = 0):
        """Return count of trees from the given location along the given integer line

        :param right:  steps right on the integer line
        :param down:  steps down on the integer line
        :param start_x:  starting X location
        :param start_y:  starting Y location

        Starting at (start_x, start_y) how many trees are encountered going
        right by right and down by down at each step on self.map?

        The map repeats, going to the right, we use modulo to calculate
        the new position at each step.
        """
        rows, cols = self.map.shape
        x_cur, y_cur = start_x, start_y

        # numpy indexes rows first (down first)
        treeval = self.map[y_cur][x_cur]
        treesum = 0
        path = [(y_cur, x_cur, "X" if treeval else "O")]  # start on tree?

        # toboggan to the bottom of the map, wrapping where needed
        while y_cur < rows:
            treeval = self.map[y_cur][x_cur]
            treesum += treeval
            path.append((y_cur, x_cur, "X" if treeval else "O"))
            x_cur = (x_cur + right) % cols
            y_cur += down

        self._lastpath = path  # store the last path for a debugging check

        return treesum

    def run_paths(self, paths):
        """Return trees hit for each path running on the passed map.

        :param paths:  iterable of (right, down) lines for toboggan
        """
        return [self.trees_in_line(right, down) for (right, down) in paths]

    @property
    def lastpath(self):
        """String representation of last path through the trees."""
        if self._lastpath is None:
            return ""
        maplist = self.mapstr[:].split()
        for xval, yval, tree in self._lastpath:
            maplist[xval] = f"{maplist[xval][:yval]}{tree}{maplist[xval][yval + 1:]}"

        return "\n".join(maplist)

    def __repr__(self):
        """String representation of instance."""
        return f"TreeMap <{id(self)}>: size:{self.map.shape}, trees:{np.sum(self.map)}"


def load_paths(fpath):
    """Return definition of toboggan paths as list of (right, down) tuples.

    :param fpath:  Path to file containing path definitions

    Definition format:

        Right 5, down 1.
        Right 7, down 1.
        Right 1, down 2.
    """
    with Path(fpath).open("r") as ifh:
        return [
            (int(x), int(y))
            for x, y in [
                _.strip()
                .replace("Right ", "")
                .replace(", down", "")
                .replace(".", "")
                .split()
                for _ in ifh.readlines()
            ]
        ]
