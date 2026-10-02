from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

# ════════════════════════════════════════════════════════
#  CHANGE THESE SETTINGS AS NEEDED
# ════════════════════════════════════════════════════════

CASE_PATH = 'path/to/your/OpenFOAM/case/result.foam'

# ── Fixed Q-criterion display range ──────────────────────
Q_MIN = 50
Q_MAX = 1100

# ── Magnitude cleanup ─────────────────────────────────────
NOISE_FLOOR = 550.0

# ── Spatial inclusion mask (coordinates: Z = span/tunnel-wall axis,
#    Y = flow axis; propeller near +Y, flow travels toward -Y) ─────────
HUB_Z       = 0.15
HUB_Y_UPPER = 0.1
TIP_Z       = 0.22

# ════════════════════════════════════════════════════════


# ── Load Case ───────────────────────────────────────────
print("\nLoading case...")
resultfoam = OpenFOAMReader(FileName=CASE_PATH)
resultfoam.CaseType = 'Decomposed Case'
resultfoam.MeshRegions = ['internalMesh',
    'patch/blatt1', 'patch/blatt2',
    'patch/blatt3', 'patch/blatt4',
    'patch/getriebe', 'patch/nabe',
    'patch/propellermutter']
    # 'patch/edelstahlring',   # <-- uncomment once you've confirmed it sits near the hub
resultfoam.CellArrays = ['Q', 'U', 'p']

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()
available_times = list(resultfoam.TimestepValues)
print(f"Available time steps ({len(available_times)}): {available_times}")

renderView1 = GetActiveViewOrCreate('RenderView')

# ── Show Geometry (reference) ────────────────────────────
ALL_PATCHES = [
    'patch/blatt1', 'patch/blatt2',
    'patch/blatt3', 'patch/blatt4',
    'patch/nabe',   'patch/getriebe',
    'patch/propellermutter'
    # 'patch/edelstahlring',
]
resultfoam.MeshRegions = ALL_PATCHES
geoDisplay = Show(resultfoam, renderView1, 'GeometryRepresentation')
geoDisplay.Representation = 'Surface'
geoDisplay.ColorArrayName = ['POINTS', '']
geoDisplay.Opacity        = 1.0
resultfoam.MeshRegions = ['internalMesh'] + ALL_PATCHES

# ── Clip 1: cylinder, keeps the region within radius 0.38 around the
#    Y-axis (tunnel bore) ─────────────────────────────────────────────
clip1 = Clip(Input=resultfoam)
clip1.ClipType = 'Cylinder'
clip1.ClipType.Center = [0.0, 0.0, 0.0]
clip1.ClipType.Axis   = [0.0, 1.0, 0.0]
clip1.ClipType.Radius = 0.38
clip1.Invert = 1

# ── Clip 2: box, trims the remaining volume to the working region ───
clip2 = Clip(Input=clip1)
clip2.ClipType = 'Box'
clip2.ClipType.Position = [-0.38, -1.0, -0.38]
clip2.ClipType.Length   = [0.76, 1.4, 0.76]
clip2.Invert = 1

# ── Merge Blocks ──────────────────────────────────────────
mergeBlocks1 = MergeBlocks(Input=clip2)

# ── Compute Q-criterion via Gradient (on the small clipped region) ──
gradient1 = Gradient(Input=mergeBlocks1)
gradient1.ScalarArray             = ['POINTS', 'U']
gradient1.ComputeGradient          = 1
gradient1.ResultArrayName          = 'Gradient'
gradient1.ComputeDivergence        = 0
gradient1.ComputeVorticity         = 0
gradient1.ComputeQCriterion        = 1
gradient1.QCriterionArrayName      = 'Q Criterion'
gradient1.ContributingCellOption   = 'Dataset Max'
gradient1.ReplacementValueOption   = 'NaN'

# ── Slice — normal to X (spanwise cut) ───────────────────
slc = Slice(Input=gradient1)
slc.SliceType        = 'Plane'
slc.SliceType.Origin = [0.0, 0.0, 0.0]
slc.SliceType.Normal = [1.0, 0.0, 0.0]

# ── Programmable Filter — tip/hub mask ──────────────────
programmableFilter1 = ProgrammableFilter(Input=slc)
programmableFilter1.Script = f"""
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa

raw_in  = self.GetInput()
raw_out = self.GetOutput()
raw_out.ShallowCopy(raw_in)
data = dsa.WrapDataObject(raw_out)

Z = data.Points[:, 2]
Y = data.Points[:, 1]
Q = np.copy(data.PointData['Q Criterion'])

# --- Magnitude cleanup: remove weak background below the noise floor ---
noise_floor = {NOISE_FLOOR}
Q[Q < noise_floor] = 0.0

# --- Spatial inclusion mask ---
HUB_Z       = {HUB_Z}
HUB_Y_UPPER = {HUB_Y_UPPER}
TIP_Z       = {TIP_Z}

hub_band = (np.abs(Z) < HUB_Z) & (Y < HUB_Y_UPPER)
tip_band = (np.abs(Z) > TIP_Z)

keep_mask = hub_band | tip_band
Q_Criterion = np.where(keep_mask, Q, 0.0)

data.PointData.append(Q_Criterion, 'Q_Criterion')
"""
programmableFilter1.CopyArrays = 1

# ── Display + fixed color range (set ONCE) ──────────────
sd = Show(programmableFilter1, renderView1, 'GeometryRepresentation')
sd.Representation = 'Surface'
ColorBy(sd, ('POINTS', 'Q_Criterion'))
sd.InterpolateScalarsBeforeMapping = 1

lut = GetColorTransferFunction('Q_Criterion')
lut.ApplyPreset('Rainbow Uniform', True)
lut.AutomaticRescaleRangeMode = 'Never'
lut.RescaleTransferFunction(Q_MIN, Q_MAX)

pwf = GetOpacityTransferFunction('Q_Criterion')
pwf.RescaleTransferFunction(Q_MIN, Q_MAX)

sd.SetScalarBarVisibility(renderView1, True)
Hide(resultfoam, renderView1)

renderView1.UseFXAA = 1

# ── Fixed camera ─────────────────────────────────────────
renderView1.CameraPosition      = [5.0, 0.0, 0.0]
renderView1.CameraFocalPoint    = [0.0, 0.0, 0.0]
renderView1.CameraViewUp        = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.8

Render()

print("\nSetup complete — Clip(cylinder) -> Clip(box) -> MergeBlocks -> Gradient -> Slice -> mask")
print(f"{len(available_times)} time steps available: {available_times[0]:.4f} to {available_times[-1]:.4f}")
print("\nNext step (manual, in the ParaView GUI):")
print("  1. Spot-check a few different time steps using the time controls")
print("  2. Confirm coloring = Q_Criterion, range fixed to", Q_MIN, "-", Q_MAX)
print("  3. File -> Save Animation")
