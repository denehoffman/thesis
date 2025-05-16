from dataclasses import dataclass
from enum import Enum
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from matplotloom import Loom
import numpy as np


class ExperimentType(Enum):
    PION_BEAM = r"$\pi$ beam"
    KAON_BEAM = r"$K^-$ beam"
    PHOTON_FUSION = r"$\gamma\gamma$ fusion"
    PROTON_BEAM = "$p$ beam"
    PHOTOPRODUCTION = "photoproduction"


class Collaboration(Enum):
    CERN = "CERN"
    BNL = "BNL"
    LRL = "LRL"
    ANL = "ANL"
    DESY = "DESY"
    ITEP = "ITEP"
    SLAC = "SLAC"
    LEP = "LEP"
    FNAL = "FNAL"
    JLAB = "JLAB"


@dataclass
class Experiment:
    year: int
    n_events: int
    experiment_type: ExperimentType
    collaboration: Collaboration


experiments = [
    Experiment(1961, 54, ExperimentType.PION_BEAM, Collaboration.CERN),
    Experiment(1962, 19, ExperimentType.PION_BEAM, Collaboration.BNL),
    Experiment(1962, 66, ExperimentType.PION_BEAM, Collaboration.LRL),
    Experiment(1966, 374, ExperimentType.PION_BEAM, Collaboration.BNL),
    Experiment(1966, 426, ExperimentType.PION_BEAM, Collaboration.LRL),
    Experiment(1967, 418, ExperimentType.PION_BEAM, Collaboration.LRL),
    Experiment(1967, 2559, ExperimentType.PION_BEAM, Collaboration.CERN),
    Experiment(1968, 1969, ExperimentType.PION_BEAM, Collaboration.ANL),
    Experiment(1975, 4820, ExperimentType.PION_BEAM, Collaboration.CERN),
    Experiment(1976, 6380, ExperimentType.PION_BEAM, Collaboration.CERN),
    Experiment(1976, 5096, ExperimentType.PION_BEAM, Collaboration.ANL),
    Experiment(1977, 410, ExperimentType.KAON_BEAM, Collaboration.CERN),
    Experiment(1980, 1278, ExperimentType.PION_BEAM, Collaboration.BNL),
    Experiment(1982, 29381, ExperimentType.PION_BEAM, Collaboration.BNL),
    Experiment(1983, 100, ExperimentType.PHOTON_FUSION, Collaboration.DESY),
    Experiment(1986, 283, ExperimentType.KAON_BEAM, Collaboration.ITEP),
    Experiment(1986, 7156, ExperimentType.PION_BEAM, Collaboration.ITEP),
    Experiment(1986, 40494, ExperimentType.PION_BEAM, Collaboration.BNL),
    Experiment(1987, 21, ExperimentType.PHOTON_FUSION, Collaboration.DESY),
    Experiment(1988, 441, ExperimentType.KAON_BEAM, Collaboration.SLAC),
    Experiment(1988, 26, ExperimentType.PHOTON_FUSION, Collaboration.DESY),
    Experiment(1995, 62, ExperimentType.PHOTON_FUSION, Collaboration.LEP),
    Experiment(1998, 11182, ExperimentType.PROTON_BEAM, Collaboration.FNAL),
    Experiment(1999, 1000, ExperimentType.PION_BEAM, Collaboration.ITEP),
    Experiment(2001, 802, ExperimentType.PHOTON_FUSION, Collaboration.LEP),
    Experiment(2003, 553, ExperimentType.PION_BEAM, Collaboration.ITEP),
    Experiment(2006, 870, ExperimentType.PHOTON_FUSION, Collaboration.LEP),
    Experiment(2006, 40553, ExperimentType.PION_BEAM, Collaboration.ITEP),
    Experiment(2018, 13500, ExperimentType.PHOTOPRODUCTION, Collaboration.JLAB),
    Experiment(2025, 77673, ExperimentType.PHOTOPRODUCTION, Collaboration.JLAB),
]

markers = {
    ExperimentType.PION_BEAM: "o",
    ExperimentType.KAON_BEAM: "v",
    ExperimentType.PHOTON_FUSION: "D",
    ExperimentType.PROTON_BEAM: "P",
    ExperimentType.PHOTOPRODUCTION: "*",
}

colors = {
    Collaboration.CERN: "tab:blue",
    Collaboration.BNL: "tab:orange",
    Collaboration.LRL: "tab:green",
    Collaboration.ANL: "tab:red",
    Collaboration.DESY: "tab:purple",
    Collaboration.ITEP: "tab:brown",
    Collaboration.SLAC: "tab:pink",
    Collaboration.LEP: "tab:gray",
    Collaboration.FNAL: "tab:olive",
    Collaboration.JLAB: "tab:cyan",
}

type_labels_used = set()
collab_labels_used = set()
type_legend = []
collab_legend = []
min_year = min(ex.year for ex in experiments)
max_year = max(ex.year for ex in experiments)


def ease_in_out(t):
    return 3 * t**2 - 2 * t**3


n_frames = 20 * (max_year - min_year)
hold_frames = 60
total_frames = n_frames + hold_frames


def get_framewise_ymax(ease_func, buffer=0.1):
    ymax_keyframes = []
    current_max = 0
    last_frame = 0

    # Collect new max points and their frames
    for i in range(total_frames):
        y = frame_to_year(i)
        visible = [ex.n_events for ex in experiments if ex.year <= y]
        if not visible:
            ymax_keyframes.append((i, 0))
            continue
        m = max(visible)
        if m > current_max:
            current_max = m
            ymax_keyframes.append((i, m * (1 + buffer)))

    # Interpolate between keyframes using easing
    framewise_ymax = [0] * total_frames
    for idx in range(len(ymax_keyframes) - 1):
        f0, y0 = ymax_keyframes[idx]
        f1, y1 = ymax_keyframes[idx + 1]
        for f in range(f0, f1):
            t = (f - f0) / (f1 - f0)
            eased = ease_func(t)
            framewise_ymax[f] = y0 + (y1 - y0) * eased
    # Fill remaining frames with last value
    f_last, y_last = ymax_keyframes[-1]
    for f in range(f_last, total_frames):
        framewise_ymax[f] = y_last

    return framewise_ymax


def frame_to_year(frame_number):
    if frame_number < n_frames:
        t = frame_number / (n_frames - 1)
        eased_t = ease_in_out(t)
        return min_year + (max_year + 1 - min_year) * eased_t
    return max_year + 1


framewise_ymax = get_framewise_ymax(ease_in_out)


def plot_frame(frame_number, loom):
    year = frame_to_year(frame_number)
    fig, ax = plt.subplots(figsize=(12, 8))
    experiments_in_year_range = [ex for ex in experiments if ex.year <= year]
    for experiment in experiments_in_year_range:
        if experiment.experiment_type not in type_labels_used:
            type_legend.append(
                Line2D(
                    [],
                    [],
                    marker=markers[experiment.experiment_type],
                    color="black",
                    linestyle="None",
                    markersize=8,
                    label=experiment.experiment_type.value,
                )
            )
            type_labels_used.add(experiment.experiment_type)

        if experiment.collaboration not in collab_labels_used:
            collab_legend.append(
                Patch(
                    facecolor=colors[experiment.collaboration],
                    edgecolor="black",
                    label=experiment.collaboration.value,
                )
            )
            collab_labels_used.add(experiment.collaboration)
        ax.scatter(
            experiment.year,
            experiment.n_events,
            color=colors[experiment.collaboration],
            marker=markers[experiment.experiment_type],
            s=100,
        )
    if frame_number >= n_frames:
        final = max(experiments, key=lambda e: e.year)
        ax.scatter(
            final.year,
            final.n_events,
            color=colors[final.collaboration],
            marker=markers[final.experiment_type],
            s=120,
            edgecolor="black",
            zorder=5,
        )
        ax.annotate(
            "This study",
            xy=(final.year, final.n_events),
            xytext=(final.year - 10, final.n_events + 0.1 * final.n_events),
            arrowprops={"facecolor": "black", "shrink": 0.05, "width": 1.5},
            fontsize=12,
            bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "black"},
        )
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of Observed Events", fontsize=12)
    legend1 = ax.legend(
        handles=type_legend,
        title="Experiment Type",
        loc="upper left",
        bbox_to_anchor=(0.01, 0.99),
        fontsize=10,
        title_fontsize=11,
    )
    ax.add_artist(legend1)

    ax.legend(
        handles=collab_legend,
        title="Collaboration",
        loc="upper left",
        bbox_to_anchor=(0.01, 0.70),
        fontsize=10,
        title_fontsize=11,
    )
    ymax = framewise_ymax[frame_number]
    ax.set_ylim(-0.1 * max(ex.n_events for ex in experiments_in_year_range), ymax)
    ax.set_xlim(min_year - 3, year)
    ax.spines["bottom"].set_position("zero")
    ax.spines["bottom"].set_color("black")
    ax.spines["bottom"].set_linewidth(1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(True)
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")
    ax.tick_params(axis="x", direction="out", length=5, width=1)
    max_ticks = 12
    current_range = int(year) - (min_year - 2)
    step = max(1, int(np.ceil(current_range / max_ticks)))
    xticks = list(range(min_year - 2, int(year) + 1, step))
    ax.set_xticks(xticks)
    ax.text(
        0.99,
        -0.08,
        f"Year: {int(year)}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=14,
        bbox={"facecolor": "white", "edgecolor": "black", "boxstyle": "round,pad=0.3"},
    )
    loom.save_frame(fig, frame_number)


from joblib import Parallel, delayed

with Loom("past_experiments.gif", fps=20, overwrite=True, parallel=True) as loom:
    Parallel(n_jobs=-1)(delayed(plot_frame)(i, loom) for i in range(total_frames))
