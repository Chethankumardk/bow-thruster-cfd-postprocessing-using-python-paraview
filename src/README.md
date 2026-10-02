# Source Code

This directory contains the Python/ParaView scripts used in the bow-thruster CFD post-processing workflow.

## Workflow Scripts

The repository contains four Python scripts covering Q-criterion calibration, final single-time-step visualization, transient Q-criterion visualization, and moving total-pressure analysis.

### `q_range_finder.py`

Single-time-step Q-criterion display-range calibration workflow.

The script evaluates candidate Q-criterion display ranges for the blade-tip, hub/junction, and combined regions before the final visualization settings are selected.

The final selected display ranges used in the project were:

- Blade-tip region: **50–600**
- Hub/junction region: **50–1200**
- Combined region: **50–1100**

> **Source note:** The exact original standalone range-finder source was not available in the retained project files. The version included in this repository is a reconstructed portfolio implementation based on the calibration procedure documented in the project report.

### `q_criterion_final.py`

Final single-time-step Q-criterion visualization workflow.

The script uses the calibrated display ranges to generate the final visualization for the selected:

- blade-tip region
- hub/junction region
- combined tip-and-hub region

The workflow includes domain clipping, Q-criterion calculation from the velocity field, an X-normal slice, spatial masking, fixed visualization settings, and screenshot export.

### `transient_q_pipeline.py`

Transient combined tip-and-hub Q-criterion post-processing workflow.

The script applies the combined Q-criterion workflow across the available CFD time steps while maintaining consistent visualization settings.

Key settings include:

- Q display range: **50–1100**
- visualization-suppression threshold: **Q = 550**
- X-normal slice
- spatial masking
- fixed camera configuration
- fixed colour range

> Q = 550 is used as a visualization-suppression threshold for visual clarity. It is not treated as a universal physical vortex boundary or as a numerically validated noise threshold.

### `pressure_moving_slice.py`

Automated total-pressure and moving-slice visualization workflow.

Total pressure is calculated as:

```text
p_total = p + 0.5 * rho * |U|^2
```

using:

```text
rho = 1025 kg/m³
```

The workflow uses a Y-normal X-Z slice that moves from:

**Y = +0.3 m to Y = -1.5 m**

with a fixed total-pressure visualization range of:

**70–140 kPa**

The CFD solution time advances while the slice position changes. Therefore, the animation combines spatial and temporal variation and should not be interpreted as material-surface or wake tracking.

## Processing Overview

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
Final Single-Time-Step Images
              |
              v
   transient_q_pipeline.py
              |
              v
Transient Combined Q-Criterion
        Visualization


Existing OpenFOAM CFD Results
              |
              v
 pressure_moving_slice.py
              |
              v
 Total-Pressure Calculation
              |
              v
Moving Y-Normal Slice Animation
```

## Running the Scripts

The scripts are intended for use with ParaView's Python environment.

Before running them, update the example OpenFOAM case path:

```python
CASE_PATH = "/path/to/your/openfoam/case/result.foam"
```

The underlying OpenFOAM CFD simulation data are not included in this repository.

## Important Note

This project focuses on automated post-processing and scientific visualization of an existing OpenFOAM bow-thruster CFD simulation.

The repository does not claim development or validation of the underlying CFD simulation itself.
