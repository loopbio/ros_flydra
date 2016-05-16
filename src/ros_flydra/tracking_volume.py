import numpy as np
import matplotlib.pyplot as plt

import roslib; roslib.load_manifest('rospy')
import rospy


#/flydra/tracking_volume/shape = {cube,sphere}
#/flydra/tracking_volume/x_min = -1
#/flydra/tracking_volume/x_max = 1
#/flydra/tracking_volume/y_min = -1
#/flydra/tracking_volume/y_max = 1
#/flydra/tracking_volume/z_min = -1
#/flydra/tracking_volume/z_max = 1
#/flydra/tracking_volume/r = 2


class _Volume(object):

    def inside(self, x, y, z):
        return True

    def draw_mpl(self, ax, in_3d=False):
        pass

    def set_bounds_mpl(self, ax, in_3d):
        xb, yb, zb = self.get_bounds()
        if in_3d:
            ax.set_zlim(*zb)
        ax.set_xlim(*xb)
        ax.set_ylim(*xb)

    def get_bounds(self):
        return (-1, 1), (-1, 1), (-1, 1)

class SphereVolume(_Volume):

    def __init__(self):
        self.rad = float(rospy.get_param('flydra/tracking_volume/r'))

    def draw_mpl(self, ax, in_3d, *args, **kwargs):
        theta = np.linspace(0, 2*np.pi, 100)
        if in_3d:
            ax.plot(self.rad*np.cos(theta), self.rad*np.sin(theta), np.zeros_like(theta), *args, **kwargs)
            ax.plot(0.05*self.rad*np.cos(theta), 0.05*self.rad*np.sin(theta), -self.rad*np.ones_like(theta), *args, **kwargs)
            ax.plot(0.05*self.rad*np.cos(theta), 0.05*self.rad*np.sin(theta), +self.rad*np.ones_like(theta), *args, **kwargs)
        else:
            ax.plot(self.rad*np.cos(theta), self.rad*np.sin(theta), *args, **kwargs)

    def get_bounds(self):
        return (-1.2*self.rad, 1.2*self.rad), (-1.2*self.rad, 1.2*self.rad), (-1.2*self.rad, 1.2*self.rad)

def get_tracking_volume():
    try:
        kind = str(rospy.get_param('flydra/tracking_volume/shape'))
    except KeyError:
        kind = ''

    if kind == 'sphere':
        return SphereVolume()
    else:
        return _Volume()

