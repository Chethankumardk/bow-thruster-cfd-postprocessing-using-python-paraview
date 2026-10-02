# Source Code

This directory is intended for the Python/ParaView scripts used in the bow-thruster CFD post-processing workflow.

## Workflow Scripts

The project uses three main scripts:

### `Task3-4_Q_range_finder.py`

Single-time-step Q-criterion display-range calibration.

Used to establish suitable visualization ranges before applying the final settings to the transient analysis.

### `tip_hub_pipeline_final.py`

Final combined tip-and-hub Q-criterion post-processing workflow.

Used for transient visualization while maintaining consistent slice, camera, spatial-selection, and colour-range settings.

### `pressure_moving_slice.py`

Total-pressure calculation and moving-slice visualization workflow.

Used to calculate total pressure from the supplied pressure and velocity fields and visualize the field using a moving Y-normal X-Z slice.

## Processing Sequence

```text
OpenFOAM CFD Results
        |
        v
Task3-4_Q_range_finder.py
Q-Range Calibration
        |
        v
tip_hub_pipeline_final.py
Transient Q-Criterion Visualization

OpenFOAM CFD Results
        |
        v
pressure_moving_slice.py
Moving Total-Pressure Visualization
