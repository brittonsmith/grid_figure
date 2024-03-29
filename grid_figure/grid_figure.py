"""
GridFigure class



"""

#-----------------------------------------------------------------------------
# Copyright (c) Britton Smith <brittonsmith@gmail.com>.  All rights reserved.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
#-----------------------------------------------------------------------------

import numpy as np
from matplotlib import pyplot

class GridFigure(object):
    def __init__(self, rows, columns,
                 top_buffer=0.1, bottom_buffer=0.1,
                 left_buffer=0.1, right_buffer=0.1,
                 vertical_buffer=0.05, horizontal_buffer=0.05,
                 square=False, figsize=(8, 8)):

        self.top_buffer = top_buffer
        self.bottom_buffer = bottom_buffer
        self.left_buffer = left_buffer
        self.right_buffer = right_buffer
        self.vertical_buffer = vertical_buffer
        self.horizontal_buffer = horizontal_buffer

        if isinstance(rows, list) or isinstance(rows, tuple):
            self.rows = rows
        else:
            self.rows = [1.] * rows
        self.n_rows = len(self.rows)        
        if isinstance(columns, list) or isinstance(columns, tuple):
            self.columns = columns
        else:
            self.columns = [1.] * columns
        self.n_columns = len(self.columns)
        self.n_panels = self.n_rows * self.n_columns

        self.panel_height = (1.0 - self.top_buffer - self.bottom_buffer -
                             ((self.n_rows-1)*self.vertical_buffer)) / \
                             sum(self.rows)
        self.panel_width = (1.0 - self.left_buffer - self.right_buffer -
                            ((self.n_columns-1)*self.horizontal_buffer)) / \
                            sum(self.columns)

        self.square = square
        self.figsize = figsize
        if square:
            pratio = figsize[1] / figsize[0]
            panel_length = min(self.panel_width,
                               pratio * self.panel_height)
            self.panel_width = panel_length
            self.panel_height = panel_length / pratio

        self.figure = pyplot.figure(figsize=figsize)
        self.panels = [None]*self.n_panels

    def add_cax(self, my_axes, side, buffer=0.02,
                length=0.95, width=0.05):
        my_pos = np.array(my_axes.get_position())

        if side == "right":
            clength = length * self.panel_height
            left = my_pos[1][0] + buffer
            bottom = my_pos[0][1] + (self.panel_height - clength) / 2
            cwidth = width * self.panel_width
            cheight = clength
        elif side == "bottom":
            clength = length * self.panel_width
            cwidth = clength
            left = my_pos[0][0] + (self.panel_width - clength) / 2
            cheight = width * self.panel_height
            bottom = my_pos[0][1] - self.figsize[1] / self.figsize[0] * buffer
        else:
            raise NotImplementedError

        my_cax = self.figure.add_axes((left, bottom, cwidth, cheight))
        return my_cax

    def _get_index(self, index):
        if (isinstance(index, tuple) or isinstance(index, list)) \
          and len(index) == 2:
            my_row, my_column = index
            if not isinstance(my_row, int) or \
              not isinstance(my_column, int):
                raise RuntimeError(
                    "index must be an integer or a sequence of two integers.")
            my_index = my_row * self.n_columns + my_column
        elif isinstance(index, int):
            my_row = index // self.n_columns
            my_column = index % self.n_columns
            my_index = index
        else:
            raise RuntimeError(
                "index must be an integer or a sequence of two integers.")
        return my_row, my_column, my_index

    def __getitem__(self, index):
        my_row, my_column, my_index = self._get_index(index)
        if self.panels[my_index] is None:
            # calculate the position of the bottom, left corner of this plot
            left_side = self.left_buffer + \
              (sum(self.columns[:my_column]) * self.panel_width) + \
              my_column * self.horizontal_buffer
            top_side = 1.0 - \
              (self.top_buffer +
               (sum(self.rows[:my_row]) * self.panel_height) +
               my_row * self.vertical_buffer)
            bottom_side = top_side - self.panel_height * self.rows[my_row]

            # create an axes object on which we will make the plot
            my_axes = self.figure.add_axes(
                (left_side, bottom_side, 
                 self.columns[my_column] * self.panel_width, 
                 self.rows[my_row] * self.panel_height))

            self.panels[my_index] = my_axes

        return self.panels[my_index]

    @property
    def top_axes(self):
        for i in range(self.n_columns):
            yield self[0, i]

    @property
    def bottom_axes(self):
        for i in range(self.n_columns):
            yield self[self.n_rows-1, i]

    @property
    def left_axes(self):
        for i in range(self.n_rows):
            yield self[i, 0]

    @property
    def right_axes(self):
        for i in range(self.n_rows):
            yield self[i, self.n_columns-1]

    def __delitem__(self, index):
        my_row, my_column, my_index = self._get_index(index)
        self.panels[my_index] = None

    def __len__(self):
        return self.n_panels

    def __iter__(self):
        for i in range(self.n_panels):
            yield self[i]
