# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def multi_slice_viewer(volume, sites, colorbar=False, **kwargs):
    remove_keymap_conflicts({'j', 'k'})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.sites = sites
    ax.index = 0
    imm = ax.imshow(volume[ax.index], **kwargs)
    ax.set_title('Site ' + str(sites[ax.index]))
    if colorbar:
        fig.colorbar(imm)
    fig.canvas.mpl_connect('key_press_event', process_key)


def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice(ax)
    elif event.key == 'k':
        next_slice(ax)
    fig.canvas.draw()


def previous_slice(ax):
    volume = ax.volume
    # wrap around using %
    ax.index = (ax.index - 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index])
    ax.set_title('Site ' + str(ax.sites[ax.index]))


def next_slice(ax):
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index])
    ax.set_title('Site ' + str(ax.sites[ax.index]))


def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)
