try:
    range = xrange
except NameError:
    range = range

import numpy as np


def simple_repr(self):  # pragma: no cover
    template = "{self.__class__.__name__}({d})"
    d = [
        "%s=%r" % (k, v) if v is not self else "(...)" for k, v in sorted(
            self.__dict__.items(), key=lambda x: x[0])
        if (not k.startswith("_") and not callable(v)) and not (k == "signal")]
    return template.format(self=self, d=', '.join(d))


class Base(object):
    __repr__ = simple_repr


def ppm_error(x, y):
    return (x - y) / y


try:
    has_plot = True
    from matplotlib import pyplot as plt

    def draw_raw(mz_array, intensity_array=None, ax=None, **kwargs):
        """Draws un-centroided profile data, visualizing continuous
        data points

        Parameters
        ----------
        mz_array : np.ndarray or tuple
            Either the m/z array to be visualized, or if `intensity_array`
            is `None`, `mz_array` will be unpacked, looking to find a sequence
            of two `np.ndarray` objects for the m/z (X) and intensity (Y)
            coordinates
        intensity_array : np.ndarray, optional
            The intensity array to be visualized. If `None`, will attempt to
            unpack `mz_array`
        ax : matplotlib.Axes, optional
            The axis to draw the plot on. If missing, a new one will be created using
            :func:`matplotlib.pyplot.subplots`
        pretty: bool, optional
            If `True`, will call :func:`_beautify_axes` on `ax`
        **kwargs
            Passed to :meth:`matplotlib.Axes.plot`

        Returns
        -------
        matplotlib.Axes
        """
        pretty = kwargs.pop("pretty", True)
        if intensity_array is None and len(mz_array) == 2:
            mz_array, intensity_array = mz_array
        if ax is None:
            fig, ax = plt.subplots(1)
        ax.plot(mz_array, intensity_array, **kwargs)
        ax.set_xlabel("m/z")
        ax.set_ylabel("Relative Intensity")
        if pretty:
            _beautify_axes(ax)
        return ax

    def peaklist_to_vector(peaklist, width=0.000001):
        mzs = []
        intensities = []
        for peak in sorted(peaklist, key=lambda x: x.mz):
            mzs.append(peak.mz - width)
            intensities.append(0.)
            mzs.append(peak.mz)
            intensities.append(peak.intensity)
            mzs.append(peak.mz + width)
            intensities.append(0.)
        return np.array(mzs), np.array(intensities)

    def draw_peaklist(peaklist, ax=None, **kwargs):
        pretty = kwargs.pop("pretty", True)
        if ax is None:
            fig, ax = plt.subplots(1)
        mz_array, intensity_array = peaklist_to_vector(peaklist)
        ax.plot(mz_array, intensity_array, **kwargs)
        ax.set_xlabel("m/z")
        ax.set_ylabel("Relative Intensity")
        if pretty:
            _beautify_axes(ax)
        return ax

    def _beautify_axes(ax):
        ax.axes.spines['right'].set_visible(False)
        ax.axes.spines['top'].set_visible(False)
        ax.yaxis.tick_left()
        ax.xaxis.tick_bottom()
        ax.xaxis.set_ticks_position('none')
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.set_ylim(0, max(ax.get_ylim()))
        return ax

except (RuntimeError, ImportError):
    has_plot = False
