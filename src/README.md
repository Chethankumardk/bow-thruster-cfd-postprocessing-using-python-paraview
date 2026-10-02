# Source Code

This directory contains the Python/ParaView scripts used in the bow-thruster CFD post-processing workflow.

## Workflow Scripts

The repository contains three main scripts.

### `Task3-4_Q_Range.py`

Single-time-step Q-criterion visualization script using the calibrated display ranges for the regions of interest.

The configured Q display ranges are:

- Blade-tip region: **50–600**
- Hub/junction region: **50–1200**
- Combined region: **50–1100**

This script supports visualization of the selected blade-tip, hub/junction, or combined region using consistent Q-criterion display settings.

### `tip_hub_pipeline_final.py`

Transient combined tip-and-hub Q-criterion post-processing workflow.

The script applies the Q-criterion workflow across the available CFD time steps while maintaining consistent visualization settings.

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

The workflow calculates total pressure from the supplied pressure and velocity fields and uses a Y-normal X-Z slice that moves through the CFD domain.

The slice moves from:

**Y = +0.3 m to Y = -1.5 m**

while the CFD solution time also advances.

## Processing Overview

```text
Existing OpenFOAM CFD Results
        |
        +----------------------+
        |                      |
        v                      v
Task3-4_Q_Range.py    pressure_moving_slice.py
        |                      |
        v                      v
Single-Time-Step       Total-Pressure &
Q Visualization        Moving-Slice Analysis
        |
        v
tip_hub_pipeline_final.py
        |
        v
Transient Combined
Q-Criterion Visualization
```

## Important Note

The underlying OpenFOAM CFD simulation is not included in this repository.

This project focuses on automated CFD post-processing and scientific visualization using Python and ParaView.
