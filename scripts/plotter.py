#! /usr/bin/env python

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

import rospy as rp
import geometry_msgs.msg as gms

import threading as thd
import dynamic_reconfigure.server as drs
import trajpub.cfg.PlotterConfig as pc


rp.init_node('plotter')

LOCK = thd.Lock()
saved_point = np.zeros(3)
NUM_POINTS = rp.get_param('num_points', 30)

plt.ion()
plt.figure()
ax = plt.gca(projection='3d')
XMIN = rp.get_param('xmin', -1.0)
XMAX = rp.get_param('xmax', 1.0)
YMIN = rp.get_param('ymin', -1.0)
YMAX = rp.get_param('ymax', 1.0)
ZMIN = rp.get_param('zmin', -1.0)
ZMAX = rp.get_param('zmax', 1.0)
ax.set_xlim((XMIN,XMAX))
ax.set_ylim((YMIN,YMAX))
ax.set_zlim((ZMIN,ZMAX))

artists = []
artists.append(ax.scatter(*(np.zeros(3).tolist())))


def reconfig_callback(config, level):
    XMIN = config["xmin"]
    XMAX = config["xmax"]
    YMIN = config["ymin"]
    YMAX = config["ymax"]
    ZMIN = config["zmin"]
    ZMAX = config["zmax"]
    LOCK.acquire()
    ax.set_xlim((XMIN,XMAX))
    ax.set_ylim((YMIN,YMAX))
    ax.set_zlim((ZMIN,ZMAX))
    LOCK.release()
    return config


def point_callback(msg):
    global saved_point
    LOCK.acquire()
    saved_point[0] = msg.x
    saved_point[1] = msg.y
    saved_point[2] = msg.z
    LOCK.release()

rp.Subscriber('point', gms.Point, point_callback)
drs.Server(pc, reconfig_callback)

RATE = rp.Rate(3e1)
while not rp.is_shutdown():
    LOCK.acquire()
    if len(artists) == NUM_POINTS:
        artists.pop(0).remove()
    artists.append(ax.scatter(*(saved_point.tolist())))
    plt.draw()
    LOCK.release()
    RATE.sleep()
