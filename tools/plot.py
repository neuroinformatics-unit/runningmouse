import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def plot_1d(data, x_label=None, y_label=None, title=None):
    plt.figure()
    plt.plot(data)
    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)


def scroll_plot(im1_in, im2_in, title=None, x_label=None, figsize=(12, 12)):

    global im1
    global im2
    im1 = im1_in
    im2 = im2_in

    t_min = 0
    t_max = im1.shape[2] - 1
    t_init = 0

    fig = plt.figure(figsize=figsize)

    #TODO: remove hard codes
    im_ax1 = plt.axes([0.1, 0.2, 0.45, 0.65], )
    im_ax2 = plt.axes([0.5, 0.2, 0.45, 0.65], )

    slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
    im_ax1.set_xticks([])
    im_ax1.set_yticks([])

    im_ax2.set_xticks([])
    im_ax2.set_yticks([])

    plt.sca(im_ax1)
    im_plot1 = plt.imshow(im1[:, :, t_init])

    plt.sca(im_ax2)
    im_plot2 = plt.imshow(im2[:, :, t_init])

    if not x_label:
        x_label='Timepoint'
    t_slider = Slider(slider_ax, x_label, t_min, t_max, valfmt="%i",
                      valinit=t_init, valstep=1)

    if title:
        plt.suptitle(title)

    def update(t):
        t = int(t)
        im_plot1.set_data(im1[:, :, t])
        im_plot2.set_data(im2[:, :, t])

        fig.canvas.draw_idle()     # redraw the plot

    t_slider.on_changed(update)
    plt.show(block=True)

