# Project Documentation

This directory is reserved for public documentation related to the bow-thruster CFD post-processing project.

## Project Scope

The project developed an automated ParaView/Python workflow for post-processing an existing OpenFOAM bow-thruster CFD simulation.

The main tasks included:

- Q-criterion visualization-range calibration
- blade-tip vortex visualization
- hub and junction vortex visualization
- transient combined Q-criterion visualization
- total-pressure calculation
- automated moving-slice visualization
- consistent camera and colour-range configuration

## Processing Workflow

The post-processing workflow is organized around three main Python/ParaView scripts:

1. `Task3-4_Q_Range.py` — single-time-step Q-criterion visualization and calibrated display settings
2. `tip_hub_pipeline_final.py` — transient combined tip-and-hub Q-criterion visualization
3. `pressure_moving_slice.py` — total-pressure calculation and automated moving-slice visualization

The source files are available in the [`src`](../src/) directory.

## Results

Selected visualization figures are available in the [`images`](../images/) directory.

Animation results and their technical settings are documented in the [`results`](../results/) directory.

## Academic Documentation

The project was completed as part of a university Software Lab in computational fluid dynamics.

The original academic report and presentation are not included in this public repository because they contain personal, academic, and administrative information.

The repository instead provides the relevant technical methodology, source code, selected visualization results, and engineering interpretation in a portfolio-friendly format.

## Scope and Limitations

This repository focuses on CFD post-processing and visualization automation.

The underlying OpenFOAM simulation is not included.

The work presented here should not be interpreted as:

- a mesh-independence study;
- solver validation;
- turbulence-model validation;
- direct cavitation prediction;
- acoustic prediction; or
- complete three-dimensional vortex tracking.

Q-criterion thresholds, spatial masks, and display ranges are visualization choices used to produce consistent and interpretable post-processing results.

For the complete public project overview, see the [main repository README](../README.md).
