"""Script to compile CR plot data into JSON and insert them into HTML template"""

import json
from pathlib import Path
from typing import TypedDict
import bs4  # type: ignore
import numpy as np


class ScatterPlotData(TypedDict):
    E: list[float]
    I: list[float]
    stat_lo: list[float]
    stat_hi: list[float]
    syst_lo: list[float]
    syst_hi: list[float]


def load_scatter_plot_data(path: Path) -> ScatterPlotData:
    E, I, stat_lo, stat_hi, syst_lo, syst_hi = np.loadtxt(
        str(path.absolute()),
        skiprows=8,
        usecols=(0, 1, 2, 3, 4, 5),
        unpack=True,
    )
    return ScatterPlotData(
        E=list(E),
        I=list(I),
        stat_lo=list(stat_lo),
        stat_hi=list(stat_hi),
        syst_lo=list(syst_lo),
        syst_hi=list(syst_hi),
    )


class DiffuseScatterPlotData(TypedDict):
    E: list[float]
    I: list[float]
    dE_lo: list[float]
    dE_hi: list[float]
    dI_lo: list[float]
    dI_hi: list[float]


def load_diffuse_scatter_plot_data(path: Path) -> DiffuseScatterPlotData:
    E, dE_lo, dE_hi, E2I, dE2I_lo, dE2I_hi = np.loadtxt(
        str(path),
        skiprows=1,
        usecols=(0, 1, 2, 3, 4, 5),
        unpack=True,
    )
    return DiffuseScatterPlotData(
        E=list(E),
        I=list(E2I / E**2),
        dE_lo=list(dE_lo),
        dE_hi=list(dE_hi),
        dI_lo=list(dE2I_lo / E**2),
        dI_hi=list(dE2I_hi / E**2),
    )


def load_inner_scatter_plot_data(path: Path) -> DiffuseScatterPlotData:
    E, E2I = np.loadtxt(
        str(path),
        skiprows=1,
        usecols=(0, 1),
        unpack=True,
    )
    return DiffuseScatterPlotData(
        E=list(E),
        I=list(E2I / E**2),
        dE_lo=list(np.zeros_like(E)),
        dE_hi=list(np.zeros_like(E)),
        dI_lo=list(np.zeros_like(E)),
        dI_hi=list(np.zeros_like(E)),
    )


class LinePlotData(TypedDict):
    E: list[float]
    I: list[float]


def load_line_plot_data(path: Path) -> LinePlotData:
    E, I = np.loadtxt(str(path.absolute()), skiprows=0, usecols=(0, 1), unpack=True)
    return LinePlotData(
        E=list(E),
        I=list(I),
    )


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    template = current_dir / "The_CR_Spectrum_template.html"
    generated = current_dir / "../plots/The_CR_Spectrum_2023.html"
    data_dir = current_dir / "../data"
    assert template.exists()

    line_plots = []
    scatter_plots = []
    diffuse_scatter_plots = []

    dir = data_dir / "allparticle"
    for filename, experiment, zorder in [
        ("Auger2019_allParticle_totalEnergy.txt", "AUGER", 10),
        ("TA_allParticle_totalEnergy.txt", "TA", 9),
        ("KASCADE_2005_SIBYLL-2.1_allParticle_totalEnergy.txt", "KASCADE", 8),
        ("NUCLEON_allParticle_totalEnergy.txt", "NUCLEON", 8),
        ("Tibet_QGSJET+HD_allParticle_totalEnergy.txt", "TIBET", 7),
        ("HAWC_allParticle_totalEnergy.txt", "HAWC", 6),
        ("IceCube_SIBYLL-2.1_allParticle_totalEnergy.txt", "ICETOP_ICECUBE", 5),
        ("TUNKA-133_allParticle_totalEnergy.txt", "TUNKA", 4),
        ("KASCADE-Grande_SIBYLL-2.1_allParticle_totalEnergy.txt", "KASCADEGrande", 3),
    ]:
        scatter_plots.append(
            {
                "experiment": experiment,
                "data": load_scatter_plot_data(dir / filename),
                "marker": "circle",
                "kind": "allparticle",
                "zorder": zorder,
            }
        )
    for filename, experiment, zorder in [
        ("allparticle_AMS02.txt", "AMS02", 1),
        ("allparticle_CREAM.txt", "CREAM", 1),
    ]:
        line_plots.append(
            {
                "experiment": experiment,
                "data": load_line_plot_data(dir / filename),
                "kind": "allparticle",
                "zorder": zorder,
            }
        )

    dir = data_dir / "protons"
    for filename, experiment, zorder in [
        ("KASCADE_2005_SIBYLL-2.1_H_totalEnergy.txt", "KASCADE", 10),
        ("H_BESS-TeV_Ek.txt", "BESS", 4),
        ("H_PAMELA_Ek.txt", "PAMELA", 5),
        ("H_AMS-02_Ek.txt", "AMS02", 6),
        ("CREAM_III_H_kineticEnergy.txt", "CREAM", 7),
        ("KASCADE-Grande_SIBYLL-2.3_H_totalEnergy.txt", "KASCADEGrande", 2),
        ("IceCube_SIBYLL-2.1_H_totalEnergy.txt", "ICETOP_ICECUBE", 1),
        ("NUCLEON_H_totalEnergy.txt", "NUCLEON", 3),
        ("CALET_H_kineticEnergy.txt", "CALET", 8),
        ("DAMPE_H_kineticEnergy.txt", "DAMPE", 9),
    ]:
        scatter_plots.append(
            {
                "experiment": experiment,
                "data": load_scatter_plot_data(dir / filename),
                "marker": "triangle-down",
                "kind": "protons",
                "zorder": zorder,
            }
        )

    dir = data_dir / "leptons"
    for filename, experiment, zorder in [
        ("AMS-02_e+e-_kineticEnergy.txt", "AMS02", 1),
        ("FERMI_e+e-_kineticEnergy.txt", "FERMI", 4),
        ("CALET_e+e-_kineticEnergy.txt", "CALET", 3),
        ("DAMPE_e+e-_kineticEnergy.txt", "DAMPE", 5),
        ("VERITAS_e+e-_totalEnergy.txt", "VERITAS", 2),
        ("HESS_e+e-_totalEnergy.txt", "HESS", 6),
    ]:
        scatter_plots.append(
            {
                "experiment": experiment,
                "data": load_scatter_plot_data(dir / filename),
                "marker": "circle",
                "kind": "leptons",
                "zorder": zorder,
            }
        )

    dir = data_dir / "antiprotons"
    for filename, experiment, zorder in [
        ("BESS-PolarII_pbar_kineticEnergy.txt", "BESS", 3),
        ("H-bar_AMS-02_Ek.txt", "AMS02", 1),
        ("PAMELA_pbar_kineticEnergy.txt", "PAMELA", 2),
    ]:
        scatter_plots.append(
            {
                "experiment": experiment,
                "data": load_scatter_plot_data(dir / filename),
                "marker": "circle",
                "kind": "antiprotons",
                "zorder": zorder,
            }
        )

    dir = data_dir / "positrons"
    for filename, experiment, zorder in [
        ("FERMI_e+_kineticEnergy.txt", "FERMI", 1),
        ("AMS-02_e+_kineticEnergy.txt", "AMS02", 2),
        ("PAMELA_e+_kineticEnergy.txt", "PAMELA", 3),
    ]:
        scatter_plots.append(
            {
                "experiment": experiment,
                "data": load_scatter_plot_data(dir / filename),
                "marker": "square",
                "kind": "positrons",
                "zorder": zorder,
            }
        )

    diffuse_scatter_plots.append(
        {
            "experiment": "FERMI",
            "data": load_diffuse_scatter_plot_data(
                data_dir / "gammas/FERMI_gammas_igrb.txt"
            ),
            "marker": "circle-open",
            "kind": "gamma-igrb",
            "zorder": 1,
        }
    )
    diffuse_scatter_plots.append(
        {
            "experiment": "FERMI",
            "data": load_inner_scatter_plot_data(
                data_dir / "gammas/FERMI_gammas_inner.txt"
            ),
            "marker": "circle-open",
            "kind": "gamma",
            "zorder": 1,
        }
    )

    diffuse_scatter_plots.append(
        {
            "experiment": "ICECUBE",
            "data": load_diffuse_scatter_plot_data(
                data_dir / "neutrinos/IceCube_neutrinos.txt"
            ),
            "marker": "circle-open",
            "kind": "neutrinos",
            "zorder": 1,
        }
    )

    data = {
        "labels": {
            "AMS02": "AMS-02",
            "AUGER": "AUGER",
            "BESS": "BESS",
            "CALET": "CALET",
            "CREAM": "CREAM",
            "DAMPE": "DAMPE",
            "FERMI": "FERMI",
            "HAWC": "HAWC",
            "HESS": "HESS",
            "ICECUBE": "ICECUBE",
            "ICETOP_ICECUBE": "ICETOP+ICECUBE",
            "KASCADE": "KASCADE",
            "KASCADEGrande": "KASCADE-Grande",
            "NUCLEON": "NUCLEON",
            "PAMELA": "PAMELA",
            "TA": "Telescope Array",
            "TIBET": "Tibet-III",
            "TUNKA": "TUNKA",
            "VERITAS": "VERITAS",
        },
        "colors": {
            "AMS02": "forestgreen",
            "AUGER": "steelblue",
            "BESS": "yellowgreen",
            "CALET": "darkcyan",
            "CREAM": "red",
            "DAMPE": "magenta",
            "FERMI": "blue",
            "HAWC": "slategray",
            "HESS": "darkorchid",
            "ICECUBE": "salmon",
            "ICETOP_ICECUBE": "cyan",
            "KASCADEGrande": "goldenrod",
            "KASCADE": "darkgoldenrod",
            "NUCLEON": "sienna",
            "PAMELA": "darkorange",
            "TA": "crimson",
            "TIBET": "indianred",
            "TUNKA": "hotpink",
            "VERITAS": "seagreen",
        },
        "kind_labels": {  # NOTE: no MathJax here, only Unicode
            "allparticle": "all",
            "protons": "p",
            "leptons": "e⁺ + e⁻",
            "positrons": "p⁺",
            "antiprotons": "p̅",
            "gamma-igrb": "γ IGRB",
            "gamma": "γ",
            "neutrinos": "ν",
        },
        "scatter_plots": scatter_plots,
        "line_plots": line_plots,
        "diffuse_scatter_plots": diffuse_scatter_plots,
    }

    html = bs4.BeautifulSoup(template.read_text(), features="html.parser")
    data_div = html.find("div", {"id": "data"})
    assert data_div is not None
    assert isinstance(data_div, bs4.Tag)
    data_div.string = json.dumps(data)
    generated.write_text(html.prettify())
