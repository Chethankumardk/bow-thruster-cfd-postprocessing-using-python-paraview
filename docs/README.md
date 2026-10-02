# Project Documentation

This directory contains public technical documentation for the bow-thruster CFD post-processing project.

## Project Scope

This project developed an automated **Python and ParaView workflow** for post-processing an existing OpenFOAM bow-thruster CFD simulation.

The main post-processing tasks included:

- Q-criterion visualization-range calibration
- blade-tip vortex visualization
- hub and junction vortex visualization
- final single-time-step Q-criterion visualization
- transient combined tip-and-hub Q-criterion visualization
- total-pressure calculation
- automated moving-slice visualization
- consistent camera and colour-range configuration

## Processing Workflow

The public post-processing workflow is organized around four Python/ParaView scripts:

1. `q_range_finder.py` — Q-criterion display-range calibration
2. `q_criterion_final.py` — final single-time-step blade-tip, hub/junction, and combined Q-criterion visualization
3. `transient_q_pipeline.py` — transient combined tip-and-hub Q-criterion visualization
4. `pressure_moving_slice.py` — total-pressure calculation and automated moving-slice visualization

The source files are available in the [`src`](../src/) directory.

### Q-Criterion Workflow

```text
Existing OpenFOAM CFD Results
        |
        v
q_range_finder.py
        |
        v
Q-Range Calibration
        |
        v
q_criterion_final.py
        |
        v
Final Single-Time-Step Visualization
        |
        v
transient_q_pipeline.py
        |
        v
Transient Combined Q-Criterion Visualization
```

The selected Q-criterion display ranges used in the project were:

| Region | Q Display Range |
|---|---:|
| Blade tip | 50–600 |
| Hub / junction | 50–1200 |
| Combined | 50–1100 |

The transient combined workflow uses a separate visualization-suppression threshold of:

**Q = 550**

> Q = 550 is used as a visualization-suppression threshold for visual clarity. It is not treated as a universal physical vortex boundary or as a numerically validated noise threshold.

### Total-Pressure Workflow

Total pressure is calculated from the supplied pressure and velocity fields using:

```text
p_total = p + 0.5 * rho * |U|^2
```

with:

```text
rho = 1025 kg/m³
```

The total-pressure visualization uses a fixed display range of:

**70–140 kPa**

A Y-normal X-Z slice moves through the CFD domain from:

**Y = +0.3 m to Y = -1.5 m**

while the CFD solution time also advances.

The resulting animation therefore contains both **spatial and temporal variation** and should be interpreted as an automated visualization sweep rather than as material-surface or wake tracking.

## Source-Code Note

The exact original standalone Q-range calibration script was not available in the retained project files.

The public `q_range_finder.py` is therefore a reconstructed portfolio implementation based on the calibration procedure documented in the project report.

The other public scripts were prepared from the retained project source code with machine-specific paths and project-specific filenames cleaned for publication.

## Results

Selected CFD visualization figures are available in the [`images`](../images/) directory.

These include:

- Q-criterion range calibration
- blade-tip vortex visualization
- hub and junction vortex visualization
- representative transient Q-criterion frames
- total-pressure visualization
- representative moving pressure-slice stages

The animation results are available in the [`results`](../results/) directory:

- `transient_q_criterion.mp4`
- `moving_total_pressure_slice.mp4`

## Academic Documentation

The project was completed as part of a university Software Lab focused on computational fluid dynamics.

The original academic report and presentation are intentionally not included in this public repository because they contain personal, academic, administrative, and course-related information.

The repository instead presents the relevant technical methodology, source code, selected visualization results, animations, engineering interpretation, and documented limitations in a portfolio-friendly format.

## Scope and Limitations

This repository focuses on **CFD post-processing, engineering automation, and scientific visualization**.

The underlying OpenFOAM simulation was supplied separately and is not included in this repository.

The work presented here should not be interpreted as:

- a mesh-independence study
- solver validation
- turbulence-model validation
- direct cavitation prediction
- acoustic prediction
- complete three-dimensional vortex tracking

Q-criterion display ranges, spatial masks, and suppression thresholds are visualization choices used to produce consistent and interpretable post-processing results.

A two-dimensional slice does not represent the complete three-dimensional vortex topology.

Because the moving pressure slice changes position while the CFD solution time advances, spatial development and temporal variation cannot be separated from that animation alone.

A visually clear CFD result should not by itself be interpreted as numerical or physical validation of the underlying simulation.

## Repository Navigation

- [`src/`](../src/) — Python/ParaView source code
- [`images/`](../images/) — selected CFD visualization results
- [`results/`](../results/) — transient animation results and technical settings
- [`README.md`](../README.md) — complete public project overview
