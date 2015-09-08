import datetime
import logging

from Tkinter import *

from astar import *
from view import Main


def center_window(r):

    width = 1000
    height = 800

    screen_width = r.winfo_screenwidth()
    screen_height = r.winfo_screenheight()

    x = (screen_width - width) / 2
    y = (screen_height - height) / 2

    r.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    """
    Main run method
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    logging.debug('Starting program at %s' % datetime.datetime.utcnow().strftime('%H:%M:%S'))

    root = Tk()
    center_window(root)
    app = Main(root)

    root.mainloop()