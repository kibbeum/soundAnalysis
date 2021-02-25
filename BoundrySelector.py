from matplotlib.widgets import RectangleSelector

"""
    Class : BoundrySelector
    - audio 범위 선택을 위한 selector class
"""
class BoundrySelector(RectangleSelector):
    def draw_shape(self, extents):
        x0, x1, y0, y1 = extents
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])
        xlim = sorted(self.ax.get_xlim())
        ylim = sorted(self.ax.get_ylim())

        xmin = max(xlim[0], xmin)
        ymin = max(ylim[0], ymin)
        xmax = min(xmax, xlim[1])
        ymax = min(ymax, ylim[1])

        if self.drawtype == 'box':
            self.to_draw.set_x(xmin)
            self.to_draw.set_y(ylim[1]*-1)
            self.to_draw.set_width(xmax - xmin)
            self.to_draw.set_height(ylim[1]*2)

        elif self.drawtype == 'line':
            self.to_draw.set_data([xmin, xmax], [ymin, ymax])


