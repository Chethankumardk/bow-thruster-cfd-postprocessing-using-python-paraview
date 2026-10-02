# Results Summary

This directory summarizes the main results and visualization settings from the automated bow-thruster CFD post-processing workflow.

The project post-processes an existing OpenFOAM simulation using Python and ParaView.

## Q-Criterion Visualization

A Q-criterion range study was used to establish consistent visualization settings for different regions of interest.

| Analysis | Selected Q Display Range |
|---|---:|
| Blade-tip region | 50–600 |
| Hub/junction region | 50–1200 |
| Combined tip and hub | 50–1100 |

For the transient combined visualization, a separate threshold of **Q = 550** was used to suppress weaker structures for visual clarity.

> **Note:** Q = 550 is a visualization-suppression threshold. It is not treated as a universal physical vortex boundary or as a numerically validated noise threshold.

## Transient Vortex Visualization

The combined tip-and-hub workflow was evaluated across the available CFD time steps while maintaining consistent:

- Q display range
- slice orientation
- spatial-selection logic
- camera configuration
- visualization settings

This allows qualitative comparison of the visible Q-criterion structures between representative transient frames.

## Total-Pressure Analysis

Total pressure was calculated using:

**p_total = p + 0.5 ρ |U|²**

with:

**ρ = 1025 kg/m³**

The visualization used a fixed total-pressure display range of:

**70–140 kPa**

## Moving Pressure Slice

A Y-normal X-Z slice was moved through the domain from:

**Y = +0.3 m → Y = -1.5 m**

The CFD time advances while the slice position changes. Therefore, the resulting sequence represents combined spatial and temporal sampling rather than automatic wake tracking.

## Visualization Results

The selected figures are available in the [`images`](../images/) directory.

The main project README provides the complete workflow description and visual results.
