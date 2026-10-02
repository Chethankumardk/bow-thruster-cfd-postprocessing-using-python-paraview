from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

# ════════════════════════════════════════════════════════
#  CHANGE THESE SETTINGS AS NEEDED
# ════════════════════════════════════════════════════════

CASE_PATH = 'path/to/your/OpenFOAM/case/result.foam'

# ── Total pressure: 'p' confirmed as static pressure in Pa (dimensions
#    [1 -1 -2 0 0 0 0]), so p_total = p + 0.5*RHO*|U|^2 uses RHO directly.
KINEMATIC_P = False
RHO         = 1025.0   # sea water, kg/m^3

# ── Fixed total-pressure display range — from manual sampling in ParaView ─
PTOT_MIN = 70000.0
PTOT_MAX = 140000.0

# ── Sweep axis: which axis the slice moves along ─────────────────────────
#    Domain bounds: X [-0.4, 0.4] (thin — blade span direction),
#                    Y [-1.5, 0.3] (long — flow/tunnel axis, confirmed via U components)
#    Flow direction confirmed: propeller near +Y, flow travels toward -Y (housing).
#    "Across-flow" = normal to the FLOW direction (Y), sweeping along Y.
SWEEP_AXIS   = 1            # 1 = y  (flow/tunnel axis)
SWEEP_START  =  0.3         # propeller / inlet side
SWEEP_END    = -1.5         # downstream, toward housing
SLICE_NORMAL = [0.0, 1.0, 0.0]   # across-flow: normal aligned with Y

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
resultfoam.CellArrays = ['U', 'p']

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
]
resultfoam.MeshRegions = ALL_PATCHES
geoDisplay = Show(resultfoam, renderView1, 'GeometryRepresentation')
geoDisplay.Representation = 'Surface'
geoDisplay.ColorArrayName = ['POINTS', '']
geoDisplay.Opacity        = 0.3   # semi-transparent so the moving slice stays visible through it
resultfoam.MeshRegions = ['internalMesh'] + ALL_PATCHES

# ── Merge Blocks ──────────────────────────────────────────
mergeBlocks1 = MergeBlocks(Input=resultfoam)

# ── Box clip — same domain restriction as your Q pipeline ────────────────
boxClip = Clip(Input=mergeBlocks1)
boxClip.ClipType = 'Box'
boxClip.ClipType.Position = [-0.4, -1.5, -0.5]
boxClip.ClipType.Length   = [0.8, 1.8, 1.0]
boxClip.Invert = 1

# ── Total pressure via Calculator ─────────────────────────
if KINEMATIC_P:
    expr = 'p + 0.5*mag(U)^2'
else:
    expr = f'p + 0.5*{RHO}*mag(U)^2'

calcPtot = Calculator(Input=boxClip)
calcPtot.ResultArrayName = 'p_total'
calcPtot.Function = expr
calcPtot.AttributeType = 'Point Data'

# ── Slice — position will be driven by an animation track below ─────────
slc = Slice(Input=calcPtot)
slc.SliceType = 'Plane'
origin = [0.0, 0.0, 0.0]
origin[SWEEP_AXIS] = SWEEP_START
slc.SliceType.Origin = origin
slc.SliceType.Normal = SLICE_NORMAL

# ── Display ────────────────────────────────────────────────
sd = Show(slc, renderView1, 'GeometryRepresentation')
sd.Representation = 'Surface'
ColorBy(sd, ('POINTS', 'p_total'))
sd.InterpolateScalarsBeforeMapping = 1

lut = GetColorTransferFunction('p_total')
lut.ApplyPreset('Cool to Warm', True)
lut.AutomaticRescaleRangeMode = 'Never'
lut.RescaleTransferFunction(PTOT_MIN, PTOT_MAX)

pwf = GetOpacityTransferFunction('p_total')
pwf.RescaleTransferFunction(PTOT_MIN, PTOT_MAX)

sd.SetScalarBarVisibility(renderView1, True)
Hide(resultfoam, renderView1)

renderView1.UseFXAA = 1

# ════════════════════════════════════════════════════════
#  ANIMATION TRACK: ties the slice's Origin[SWEEP_AXIS] to the animation
#  scene's time, so Save Animation moves the slice automatically alongside
#  the timestep playback — no manual dragging, no Python export loop needed.
# ════════════════════════════════════════════════════════

# Animate over the scene's normalized time range [0, 1], which spans
# whatever start/end frame you set in the Animation View (usually your
# full timestep range if UpdateAnimationUsingDataTimeSteps() was used).
sliceTrack = GetAnimationTrack('Origin', index=SWEEP_AXIS, proxy=slc.SliceType)
sliceTrack.TimeMode = 'Normalized'

startKey = CompositeKeyFrame()
startKey.KeyTime = 0.0
startKey.KeyValues = [SWEEP_START]

endKey = CompositeKeyFrame()
endKey.KeyTime = 1.0
endKey.KeyValues = [SWEEP_END]

sliceTrack.KeyFrames = [startKey, endKey]

# ── Fixed camera — view along the FLOW axis (Y) so the slice cross-section
#    (an X-Z plane) is seen face-on as it sweeps, not edge-on ──────────────
renderView1.CameraPosition      = [0.0, 5.0, 0.0]
renderView1.CameraFocalPoint    = [0.0, 0.0, 0.0]
renderView1.CameraViewUp        = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.5

Render()

print("\nSetup complete — slice will sweep automatically from")
print(f"  axis {SWEEP_AXIS}: {SWEEP_START} -> {SWEEP_END}")
print("across the full animation duration, tied to the Animation Scene.")
print(f"{len(available_times)} time steps available: {available_times[0]:.4f} to {available_times[-1]:.4f}")
print("\nNext step (manual, in the ParaView GUI):")
print("  1. Open the Animation View (View -> Animation View) and confirm")
print("     you see BOTH a 'TimeKeeper' track (playing timesteps) AND a")
print("     'Slice1 - Origin' track (moving the plane) listed together")
print("  2. Scrub the timeline manually first to sanity-check the slice")
print("     actually moves and p_total looks reasonable at a few points")
print("  3. Confirm coloring = p_total, range fixed to", PTOT_MIN, "-", PTOT_MAX)
print("  4. File -> Save Animation")
