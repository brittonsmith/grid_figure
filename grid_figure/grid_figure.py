from matplotlib import pyplot

class GridFigure(object):
    def __init__(self, rows, columns,
                 top_buffer=0.1, bottom_buffer=0.1,
                 left_buffer=0.1, right_buffer=0.1,
                 vertical_buffer=0.05, horizontal_buffer=0.05,
                 figsize=(8, 8)):

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

        self.figure = pyplot.figure(figsize=figsize)

    def __len__(self):
        return self.n_panels

    def __iter__(self):
        for i in range(self.n_panels):
            # get the row and column number
            my_row = i / self.n_columns
            my_column = i % self.n_columns

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

            yield my_axes
