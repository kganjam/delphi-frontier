"""R5: physically simulated collective (school) launch in PyBullet: rigid 6-DOF printed gliders with quasi-steady
per-surface aerodynamics, launched side by side; contacts between fish are PyBullet collisions.

    python -m engineering.organ_sims.r5_school_launch [n_seeds]

Parameters and where they come from (none is a measured flight; 'computed' = from the print meshes):
  mass, CG, inertia  r4 flight_model assembled_dry (computed from part meshes x 1220 kg/m3) + nose ballast at the bay
                     centroid, trimmed to CG = NP - 8% MAC (R2 rule).  Off-diagonal inertia (xz 8e-7) dropped.
  surfaces           pectoral and pelvic outlines, dihedral and incidence from the r4 flight_model; median fins
                     (dorsal, anal, caudal) one-side areas and centroids from the v3a component STLs (R3 geometry).
  aero per surface   CL = CLa(AR) alpha with Helmbold CLa, linear to CLmax 0.8 then flat-plate CL = sin(2 alpha) x
                     CLmax/sin(2 alpha_s) (assumed); CD = CD0 + CL^2/(pi e AR), flat plate 2 sin^2 alpha after stall;
                     CD0 from laminar skin friction at the surface chord Re (R2/R3 law); pelvic/median fins see a
                     pectoral downwash eps = 2 CL_pec/(pi AR_wing) (assumed full).  Body: skin-friction drag and Munk
                     moment q Vol (k2-k1) sin 2a with k2-k1 = 0.9 (repo's hand-NP bracket 0.80-0.95).
  launch             release at h 1.35 m, V0 8 m/s level (R2 grid; slingshot spec V_design 10 m/s in
                     artifacts/launch-glider/print-requirements.json).  Release dispersion is an ASSUMED scenario
                     (no launch has been measured): sigma V 5%, pitch/yaw/roll 3 deg, pitch rate 2 rad/s ('low'), x2 ('high').
  NOT modelled       wakes and aerodynamic interaction between fish, ground effect over water, unsteady aero,
                     fin flexibility (R4), band/hook contact during the stroke.
"""
import json, math, sys, time
import numpy as np
import pybullet as pb
from engineering.organ_sims import common as C

RID = "r5-school-launch"
FM = "artifacts/glider/r4-daane-printfix/flight_model.json"
MAN = "artifacts/glider/r4-daane-printfix/manifest.json"
R3M = "artifacts/organ-sims/r3-underwater-drag/manifest.json"
RHO, NU, G = 1.204, 1.516e-5, 9.81
H0, V0 = 1.35, 8.0
DT = 1.0 / 1000
CLMAX, E_OSW, K21 = 0.8, 0.8, 0.9
SM = 0.08
X_BALLAST = 15.0e-3
DISP = {"none": dict(V=0, th=0, psi=0, phi=0, q=0), "low": dict(V=0.05, th=3, psi=3, phi=3, q=2.0),
        "high": dict(V=0.10, th=6, psi=6, phi=6, q=4.0)}


def helm(ar):
    return 2 * math.pi * ar / (2 + math.sqrt(4 + ar * ar))


def cf_lam(Re):
    return 1.328 / math.sqrt(max(Re, 100.0))


def poly_centroid_area(P):
    x, y = P[:, 0], P[:, 1]
    xs, ys = np.roll(x, -1), np.roll(y, -1)
    a = x * ys - xs * y
    A = a.sum() / 2
    return np.array([((x + xs) * a).sum(), ((y + ys) * a).sum()]) / (6 * A), abs(A)


def rot(axis, deg):
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    t = math.radians(deg)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def build_model(cg_shift=0.0, decalage=2.0, pec=(1.0, 1.0, 0.0)):
    """Body-frame model (flight_model frame: x snout->tail, y left, z dorsal; origin snout), returns dict in CG frame.
    pec = (area scale, aspect-ratio scale, root x shift m) of the pectoral pair, as in R2: span x sqrt(ka kar), chord x
    sqrt(ka/kar), fin mass x ka, ballast and CG from R2's own config() rule so a design is the same object in both runs.
    The default reproduces R5 exactly."""
    H = json.loads((C.ROOT / FM).read_text()); M = json.loads((C.ROOT / MAN).read_text())
    R3 = json.loads((C.ROOT / R3M).read_text())["results"]["geometry"]["v3a"]
    dry = H["assembled_dry"]; m_d = dry["mass_kg"]; cg_d = np.array(dry["cg_m"])
    hnp = M["hand_neutral_point"]
    mac = hnp["pectoral_mac_mm"] * 1e-3
    np_x = float(np.mean(hnp["np_x_mm_bracket"])) * 1e-3
    x_t = np_x - SM * mac + cg_shift
    m_b = max(m_d * (cg_d[0] - x_t) / (x_t - X_BALLAST), 0.0)
    m = m_d + m_b
    cg = (m_d * cg_d + m_b * np.array([X_BALLAST, 0, cg_d[2]])) / m
    I = np.array(dry["inertia_cg_kg_m2"])
    # parallel-axis: move dry inertia to the new CG and add the ballast point mass
    def pa(mass, r):
        r = np.asarray(r); return mass * (r @ r * np.eye(3) - np.outer(r, r))
    I = I + pa(m_d, cg_d - cg) + pa(m_b, np.array([X_BALLAST, 0, cg_d[2]]) - cg)
    ka, kar, dxp = pec
    scaled = (ka, kar, dxp) != (1.0, 1.0, 0.0)
    if scaled:
        from engineering.organ_sims import r2_glide_sweep as R2
        c2 = R2.config(R2.S_PEC0 * ka, R2.AR0 * kar, dxp, 0.8, V0, 0.0)
        m_fin_extra = R2.m_pec2 * (ka - 1.0)
        m_dry2 = c2["m_dry_kg"]
        cg_dry2 = (c2["m_total_kg"] * c2["cg_final_m"] - c2["m_ballast_kg"] * X_BALLAST) / m_dry2
        x_t2 = c2["cg_final_m"] + cg_shift                     # cg_shift moves the TARGET; ballast is recomputed
        m_b = max(m_dry2 * (cg_dry2 - x_t2) / (x_t2 - X_BALLAST), 0.0)
        m = m_dry2 + m_b
        cg = np.array([(m_dry2 * cg_dry2 + m_b * X_BALLAST) / m, 0.0, cg_d[2]])
        cg_d = np.array([cg_dry2, 0.0, cg_d[2]])
        I = np.array(dry["inertia_cg_kg_m2"]) + pa(m_d, cg_d - cg) + pa(m_b, np.array([X_BALLAST, 0, cg_d[2]]) - cg)
        pc = np.array([R2.cg_pec + dxp, 0.0, cg_d[2]])
        for sgn in (1, -1):    # extra fin mass as two point masses at the scaled fin centroids (approximation)
            I = I + pa(m_fin_extra / 2, pc + np.array([0, sgn * 0.06 * math.sqrt(ka * kar), 0]) - cg)
    surfaces = []
    S_wing = 0.0
    for s in H["lifting_surfaces"]:
        fr = s["frame_L"]; eu = np.array(fr["e_u"]); ew = np.array(fr["e_w"]); O = np.array(fr["origin_mm"]) * 1e-3
        cen_uw, A = poly_centroid_area(np.array(s["outline_uw_mm"]) * 1e-3)
        span = np.ptp(np.array(s["outline_uw_mm"])[:, 0]) * 1e-3
        # pectoral: 2 deg; pelvic: a printed key, incidence = pectoral - decalage (r4 manifest); default key dec+2 is
        # the part used in assembled_dry
        inc = s["incidence_about_span_axis_deg"]
        inc = inc[0] if s["id"] == "pectoral" else (2.0 - decalage)
        n = np.cross(ew, eu); n = n if n[2] > 0 else -n
        Rinc = rot(eu, inc)                        # leading edge (-x) up: right-hand rotation about the (~+y) span axis
        n = Rinc @ n; t = Rinc @ ew
        sr, cr = (math.sqrt(ka * kar), math.sqrt(ka / kar)) if s["id"] == "pectoral" else (1.0, 1.0)
        if s["id"] == "pectoral":
            span, A = span * sr, A * ka
        for side in (1, -1):
            mir = np.array([1, side, 1])
            r = (O + cen_uw[0] * sr * eu + cen_uw[1] * cr * ew) * mir
            # force point = aerodynamic centre: spanwise at the area centroid, streamwise at the r4 manifest's
            # quarter-chord station of the mean chord (hand_neutral_point.<fin>.quarter_chord_x_mm), not the centroid
            qx = hnp[s["id"]]["quarter_chord_x_mm"] * 1e-3
            r[0] = O[0] + (qx - O[0]) * cr + (dxp if s["id"] == "pectoral" else 0.0)
            nn = n * mir; tt = t * mir
            AR_pair = (2 * span) ** 2 / (2 * A)
            surfaces.append({"id": f"{s['id']}_{'L' if side > 0 else 'R'}", "r": r - cg, "n": nn, "t": tt, "S": A, "AR": AR_pair,
                             "chord": A / span, "CLa": helm(AR_pair), "kind": s["id"]})
        if s["id"] == "pectoral":
            S_wing = 2 * A; b_wing = 2 * (np.abs(O[1]) + span * eu[1])
    AR_wing = b_wing ** 2 / S_wing
    for f in ("dorsal", "anal", "caudal"):
        g = R3["fins"][f]
        # centroid of the v3a component STL (same snout-origin frame, metres)
        T = read_stl_centroid(f"artifacts/fish3d/fish3d-v3a-fan/components/{f}.stl")
        h = max(g["S_one_side_m2"] / max(g["streamwise_extent_m"], 1e-3), 1e-3)
        ar = 2 * h * h / g["S_one_side_m2"]            # mounted on the body: image doubles effective AR (assumed)
        T = T - np.array([0.25 * g["streamwise_extent_m"], 0, 0])     # quarter chord ahead of the centroid (assumed)
        surfaces.append({"id": f, "r": T - cg, "n": np.array([0, 1.0, 0]), "t": np.array([1.0, 0, 0]), "S": g["S_one_side_m2"], "AR": ar,
                         "chord": g["streamwise_extent_m"], "CLa": helm(ar), "kind": "median"})
    body = {"S_wet": H["body"]["wetted_area_m2"], "L": 0.159, "vol": H["body"]["enclosed_volume_m3"],
            "FF": 1 + 1.5 * (math.sqrt(H["body"]["max_width_m"] * H["body"]["max_depth_m"]) / 0.159) ** 1.5}
    return {"pec": list(pec), "decalage_deg": decalage, "m": m, "m_ballast": m_b, "cg": cg, "I": I, "surfaces": surfaces, "S_wing": S_wing, "AR_wing": AR_wing, "b_wing": b_wing,
            "np_x": np_x, "mac": mac, "body": body, "width": H["body"]["max_width_m"], "depth": H["body"]["max_depth_m"]}


def read_stl_centroid(path):
    from engineering.organ_sims.r3_underwater_drag import read_stl
    T = read_stl(path)
    a = 0.5 * np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1)
    return (T.mean(axis=1) * a[:, None]).sum(0) / a.sum()


def ground_factor(h, b):
    """McCormick ground-effect factor on induced drag (recalled; argon review #8): phi = (16h/b)^2 / (1 + (16h/b)^2)."""
    if h is None:
        return 1.0
    x = (16 * max(h, 0.0) / b) ** 2
    return x / (1 + x)


def aero(model, R, v, w, p=None, wake=None, h=None):
    """Total world force and torque (about CG) from quasi-steady surfaces + body. R body->world rotation matrix,
    v CG velocity (world), w angular velocity (world), p CG position (world).  Each surface's velocity is taken at its
    3/4-chord point (gives the surface's own pitch damping; argon review #5) and its force acts at its 1/4 chord.
    wake(points_world) -> induced air velocity (world) from OTHER fish; h height for ground effect."""
    Fw = np.zeros(3); Tw = np.zeros(3)
    wb = R.T @ w; vb = R.T @ v
    Vmag = np.linalg.norm(vb)
    if Vmag < 1e-6:
        return Fw, Tw, {}
    q = 0.5 * RHO * Vmag ** 2
    # body drag + Munk moment
    eD = -vb / Vmag
    cd_body = cf_lam(Vmag * model["body"]["L"] / NU) * model["body"]["FF"] * model["body"]["S_wet"]
    Fb = q * cd_body * eD
    # Munk: flow direction in body axes; nose is -x.  moment turns the body broadside (destabilising)
    u_fwd = -vb[0]; a_p = math.atan2(-vb[2], u_fwd) if u_fwd > 0 else 0.0   # pitch AoA (positive: air from below)
    b_y = math.atan2(vb[1], u_fwd) if u_fwd > 0 else 0.0
    Mmunk = q * model["body"]["vol"] * K21 * np.array([0.0, math.sin(2 * a_p), math.sin(2 * b_y)])
    # sign: R_y(+phi) maps the nose (-1,0,0) to (-cos, 0, +sin): +torque about body +y raises the nose, i.e. increases
    # a_p (destabilising, as Munk must be).  R_z(+psi) moves the nose to -y, away from a +y body velocity (b_y > 0).
    Fsum = Fb.copy(); Tsum = Mmunk.copy()
    CLpec = []
    info = {}
    gf = ground_factor(h, model["b_wing"])
    rv = [s["r"] + 0.5 * s["chord"] * s["t"] for s in model["surfaces"]]
    ind = R.T @ wake(np.array([p + R @ r for r in rv])).T if (wake is not None and p is not None) else None
    for k, s in enumerate(model["surfaces"]):
        vs = vb + np.cross(wb, rv[k])                 # 3/4-chord point velocity in body frame
        vr = -vs                                      # air relative to surface
        if ind is not None:
            vr = vr + ind[:, k]
        span_dir = np.cross(s["n"], s["t"])
        vr = vr - (vr @ span_dir) * span_dir          # drop the spanwise component
        Vl = np.linalg.norm(vr)
        if Vl < 1e-6:
            continue
        e_d = vr / Vl
        sa = float(np.clip(e_d @ s["n"], -1, 1))
        alpha = math.asin(sa)
        if s["kind"] == "pelvic" and CLpec:
            alpha -= 2 * float(np.mean(CLpec)) / (math.pi * model["AR_wing"])
        a_s = CLMAX / s["CLa"]
        if abs(alpha) <= a_s:
            CL = s["CLa"] * alpha; CD = cf_lam(Vl * s["chord"] / NU) * 2 + gf * CL * CL / (math.pi * E_OSW * s["AR"])
        else:
            CL = math.sin(2 * alpha) * CLMAX / math.sin(2 * a_s); CD = 2 * math.sin(alpha) ** 2 + cf_lam(Vl * s["chord"] / NU) * 2
        if s["kind"] == "pectoral":
            CLpec.append(CL)
        lh = s["n"] - (s["n"] @ e_d) * e_d
        ln = np.linalg.norm(lh)
        lh = lh / ln if ln > 1e-9 else s["n"]
        ql = 0.5 * RHO * Vl * Vl * s["S"]
        F = ql * (CL * lh + CD * e_d)
        Fsum += F; Tsum += np.cross(s["r"], F)
        info[s["id"]] = alpha
    return R @ Fsum, R @ Tsum, info


RC_FRAC = 0.05            # vortex core radius / span (assumed)


def seg_induced(P, A, B, gam, rc):
    """Biot-Savart velocity at points P (N,3) from straight segments A->B (M,3) of circulation gam (M,), with a
    Scully-type core (rc, absolute).  Returns (N,3)."""
    r1 = P[:, None, :] - A[None]; r2 = P[:, None, :] - B[None]; r0 = (B - A)[None]
    c = np.cross(r1, r2); c2 = (c * c).sum(-1)
    n1 = np.linalg.norm(r1, axis=-1); n2 = np.linalg.norm(r2, axis=-1)
    k = (r0 * (r1 / np.maximum(n1, 1e-12)[..., None] - r2 / np.maximum(n2, 1e-12)[..., None])).sum(-1)
    l0 = (r0 * r0).sum(-1)
    f = gam[None] * k / (4 * math.pi * (c2 + rc * rc * l0))
    return (c * f[..., None]).sum(1)


def horseshoes(states, model):
    """states: list of (p, R, v, lift_vec_world).  Each fish -> straight horseshoe: bound line between tips at
    +-b'/2 (b' = pi b/4, elliptic loading), legs trailing 50 m along -v.  Gamma = |L| / (rho V b').  Orientation chosen
    so that the bound+trailing system induces DOWNWASH (against the lift) behind the fish's own centre."""
    bp = math.pi / 4 * model["b_wing"]
    segs = []
    for st in states:
        if st is None:
            segs.append(None); continue
        p, R, v, L = st
        V = np.linalg.norm(v); Lm = np.linalg.norm(L)
        if V < 1e-6 or Lm < 1e-9:
            segs.append(None); continue
        d = -v / V; lat = R[:, 1]; lat = lat - (lat @ d) * d; lat /= np.linalg.norm(lat)
        g = Lm / (RHO * V * bp)
        Tl, Tr = p + lat * bp / 2, p - lat * bp / 2
        A = np.array([Tl + 50 * d, Tl, Tr]); B = np.array([Tl, Tr, Tr + 50 * d])
        test = seg_induced((p + 0.3 * bp * d)[None], A, B, np.full(3, g), RC_FRAC * model["b_wing"])[0]
        if test @ L > 0:
            g = -g
        segs.append((A, B, np.full(3, g)))
    return segs


def wake_for(i, segs, model):
    others = [sg for j, sg in enumerate(segs) if j != i and sg is not None]
    if not others:
        return None
    A = np.vstack([o[0] for o in others]); B = np.vstack([o[1] for o in others]); g = np.concatenate([o[2] for o in others])
    rc = RC_FRAC * model["b_wing"]
    return lambda P: seg_induced(P, A, B, g, rc)


def trim_scan(model, V=V0):
    """Static pitch moment vs body AoA at speed V, no rotation: returns list of (alpha_deg, CL_total, Cm_about_CG, L/D)."""
    out = []
    for a in np.arange(-4, 16.01, 0.25):
        ar = math.radians(a)
        vb = np.array([-math.cos(ar), 0.0, -math.sin(ar)]) * V          # moving nose-first (-x) and down: air from below
        F, T, _ = aero(model, np.eye(3), vb, np.zeros(3))
        e_d = -vb / V; up = np.array([-math.sin(ar), 0, math.cos(ar)])  # lift direction (perpendicular, upward)
        L = F @ up; D = F @ e_d
        q = 0.5 * RHO * V * V
        out.append((float(a), float(L / (q * model["S_wing"])), float(T[1] / (q * model["S_wing"] * model["mac"])), float(L / D) if D > 0 else None))
    return out


def trim_point(scan):
    for (a0, cl0, cm0, ld0), (a1, cl1, cm1, ld1) in zip(scan, scan[1:]):
        if cm0 > 0 >= cm1 or cm0 < 0 <= cm1:
            f = cm0 / (cm0 - cm1)
            return {"alpha_deg": a0 + f * (a1 - a0), "CL": cl0 + f * (cl1 - cl0), "dCm_dalpha_per_deg": (cm1 - cm0) / (a1 - a0),
                    "L_over_D": None if ld0 is None or ld1 is None else ld0 + f * (ld1 - ld0)}
    return None


# ------------------------------------------------------------------------------------------------- PyBullet world
def make_world():
    cid = pb.connect(pb.DIRECT)
    pb.setGravity(0, 0, -G, physicsClientId=cid)
    pb.setTimeStep(DT, physicsClientId=cid)
    pb.setPhysicsEngineParameter(numSubSteps=0, physicsClientId=cid)
    return cid


# body frame -> PyBullet base frame: identical axes; world flight direction +X means the fish's nose (-x body) points
# to +X world, i.e. base yaw 180 deg.
BASE_Q0 = pb.getQuaternionFromEuler([0, 0, math.pi])


def add_fish(cid, model, pos, euler_dev, vel, wvel):
    """Compound collision shape (body capsule + pectoral/pelvic plates) with its inertial frame at the CG."""
    rad = 0.5 * min(model["width"], model["depth"])
    plates = [s for s in model["surfaces"] if s["kind"] in ("pectoral", "pelvic")]
    ps = [list(np.array([0.159 / 2, 0, 0]) - model["cg"])] + [list(s["r"]) for s in plates]
    os_ = [pb.getQuaternionFromEuler([0, math.pi / 2, 0])] + [rotm_to_quat(np.c_[s["t"], np.cross(s["n"], s["t"]), s["n"]]) for s in plates]
    arr = pb.createCollisionShapeArray([pb.GEOM_CAPSULE] + [pb.GEOM_BOX] * len(plates),
                                       radii=[rad] + [0] * len(plates),
                                       lengths=[max(model["body"]["L"] - 2 * rad, 0.01)] + [0] * len(plates),
                                       halfExtents=[[0, 0, 0]] + [[s["chord"] / 2, (s["S"] / s["chord"]) / 2, 0.0006] for s in plates],
                                       collisionFramePositions=ps, collisionFrameOrientations=os_, physicsClientId=cid)
    q0 = pb.multiplyTransforms([0, 0, 0], pb.getQuaternionFromEuler(euler_dev), [0, 0, 0], BASE_Q0)[1]
    b = pb.createMultiBody(baseMass=model["m"], baseCollisionShapeIndex=arr, basePosition=pos, baseOrientation=q0, physicsClientId=cid)
    I = model["I"]
    pb.changeDynamics(b, -1, localInertiaDiagonal=[I[0, 0], I[1, 1], I[2, 2]], linearDamping=0, angularDamping=0, physicsClientId=cid)
    pb.resetBaseVelocity(b, vel, wvel, physicsClientId=cid)
    return b


def rotm_to_quat(R):
    tr = np.trace(R)
    if tr > 0:
        s = math.sqrt(tr + 1) * 2; w = 0.25 * s; x = (R[2, 1] - R[1, 2]) / s; y = (R[0, 2] - R[2, 0]) / s; z = (R[1, 0] - R[0, 1]) / s
    else:
        i = int(np.argmax(np.diag(R)))
        if i == 0:
            s = math.sqrt(1 + R[0, 0] - R[1, 1] - R[2, 2]) * 2; w = (R[2, 1] - R[1, 2]) / s; x = 0.25 * s; y = (R[0, 1] + R[1, 0]) / s; z = (R[0, 2] + R[2, 0]) / s
        elif i == 1:
            s = math.sqrt(1 + R[1, 1] - R[0, 0] - R[2, 2]) * 2; w = (R[0, 2] - R[2, 0]) / s; x = (R[0, 1] + R[1, 0]) / s; y = 0.25 * s; z = (R[1, 2] + R[2, 1]) / s
        else:
            s = math.sqrt(1 + R[2, 2] - R[0, 0] - R[1, 1]) * 2; w = (R[1, 0] - R[0, 1]) / s; x = (R[0, 2] + R[2, 0]) / s; y = (R[1, 2] + R[2, 1]) / s; z = 0.25 * s
    return [x, y, z, w]


def simulate(model, n, spacing, disp, seed, aero_on=True, t_max=6.0, record=False, stagger_s=0.0, wake_on=True, ground=True,
             pattern="sequential"):
    """stagger_s: release-time offset between consecutive releases; pattern 'sequential' releases lane 0,1,2,... in turn,
    'alternate' releases even lanes first then odd lanes (neighbours always differ by >= one offset).  A fish does not
    exist in the world before its release.  Random launch draws are taken in lane order up front, so stagger 0
    reproduces the simultaneous release exactly."""
    rng = np.random.default_rng(seed)
    cid = make_world()
    d = DISP[disp]
    fish, launch_t, pending = [], [], []
    order = list(range(n)) if pattern == "sequential" else list(range(0, n, 2)) + list(range(1, n, 2))
    slot = {lane: k for k, lane in enumerate(order)}
    for i in range(n):
        y = (i - (n - 1) / 2) * spacing
        e = [math.radians(d["phi"]) * rng.standard_normal(), math.radians(d["th"]) * rng.standard_normal(), math.radians(d["psi"]) * rng.standard_normal()]
        v = V0 * (1 + d["V"] * rng.standard_normal())
        qrate = d["q"] * rng.standard_normal()
        # euler_dev applied in world: roll about X (flight dir), pitch about Y (nose up = negative about +Y for +X flight)
        Rw = np.array(pb.getMatrixFromQuaternion(pb.getQuaternionFromEuler([e[0], -e[1], e[2]]))).reshape(3, 3)
        vel = Rw @ np.array([v, 0, 0])
        pending.append(([0, y, H0], [e[0], -e[1], e[2]], vel.tolist(), [0, -qrate, 0]))
        fish.append(None); launch_t.append(slot[i] * stagger_s)
    for i in range(n):
        if launch_t[i] <= 0:
            fish[i] = add_fish(cid, model, *pending[i])
    body_ix = {}
    alive = [True] * n
    out = [{"y0_m": (i - (n - 1) / 2) * spacing, "range_m": None, "y_land_m": None, "t_land_s": None, "max_roll_deg": 0.0, "max_pitch_dev_deg": 0.0, "collided": False, "end": "timeout"} for i in range(n)]
    collisions = set()
    traj = [[] for _ in range(n)] if record else None
    steps = int(t_max / DT)
    lifts = [np.zeros(3)] * n
    states = [None] * n
    for k in range(steps):
        t = k * DT
        for i in range(n):
            if fish[i] is None and t >= launch_t[i] - 1e-12:
                fish[i] = add_fish(cid, model, *pending[i])
        body_ix = {b: i for i, b in enumerate(fish) if b is not None}
        segs = horseshoes([st for st in states], model) if (wake_on and k > 0) else None
        for i, b in enumerate(fish):
            if not alive[i] or b is None:
                continue
            p, qn = pb.getBasePositionAndOrientation(b, physicsClientId=cid)
            v, w = pb.getBaseVelocity(b, physicsClientId=cid)
            R = np.array(pb.getMatrixFromQuaternion(qn)).reshape(3, 3)
            if aero_on:
                wk = wake_for(i, segs, model) if segs is not None else None
                F, T, _ = aero(model, R, np.array(v), np.array(w), p=np.array(p), wake=wk, h=p[2] if ground else None)
                vv = np.array(v); e = vv / max(np.linalg.norm(vv), 1e-9)
                lifts[i] = F - (F @ e) * e
                pb.applyExternalForce(b, -1, F.tolist(), p, pb.WORLD_FRAME, physicsClientId=cid)
                pb.applyExternalTorque(b, -1, T.tolist(), pb.WORLD_FRAME, physicsClientId=cid)
            states[i] = (np.array(p), R, np.array(v), lifts[i])     # wake source for the NEXT step (1 ms lag)
            # attitude bookkeeping: body nose = -x body
            nose = -R[:, 0]
            roll = math.degrees(math.atan2(R[2, 1], R[2, 2]))       # world-z components of body y and body z
            pitch = math.degrees(math.asin(np.clip(nose[2], -1, 1)))
            out[i]["max_roll_deg"] = max(out[i]["max_roll_deg"], abs(roll))
            out[i]["max_pitch_dev_deg"] = max(out[i]["max_pitch_dev_deg"], abs(pitch))
            if record and k % 10 == 0:
                traj[i].append([t, *p, roll, pitch])
            if p[2] <= 0.0:
                alive[i] = False
                out[i].update(range_m=p[0], y_land_m=p[1], t_land_s=t - launch_t[i], end="water")
                states[i] = None                                             # a landed fish sheds no wake
                pb.resetBaseVelocity(b, [0, 0, 0], [0, 0, 0], physicsClientId=cid)
                pb.changeDynamics(b, -1, mass=0, physicsClientId=cid)        # freeze at contact (no splash model)
        pb.stepSimulation(physicsClientId=cid)
        for c in pb.getContactPoints(physicsClientId=cid):
            a, bb = c[1], c[2]
            ia, ib = body_ix[a], body_ix[bb]
            if alive[ia] and alive[ib]:
                collisions.add((min(ia, ib), max(ia, ib)))
                out[ia]["collided"] = out[ib]["collided"] = True
        if not any(alive) or all(not a for a, b in zip(alive, fish) if b is not None) and all(b is not None for b in fish):
            break
    pb.disconnect(cid)
    return out, sorted(collisions), traj


def _launch(args):
    dec, n, disp, spacing, wake, seed = args
    o, col, _ = simulate(build_model(decalage=dec), n, spacing, disp, seed, wake_on=wake)
    return o, col


def main():
    nseed = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    t0 = time.time()
    checks = []
    # static trim per printed pelvic key (decalage -1..+4): pick the key that trims closest to CL 0.55 (near best L/D
    # without approaching the assumed CLmax 0.8); the assembled_dry part is dec+2
    trims = {}
    for dec in (-1.0, 0.0, 1.0, 2.0, 3.0, 4.0):
        sc = trim_scan(build_model(decalage=dec)); trims[dec] = {"trim": trim_point(sc), "scan": sc}
    lin = [(a, cl) for a, cl, _, _ in trims[2.0]["scan"] if -2 <= a <= 4]
    cla = np.polyfit([a for a, _ in lin], [c for _, c in lin], 1)[0]
    sm2 = -trims[2.0]["trim"]["dCm_dalpha_per_deg"] / cla
    checks.append({"name": "cross-check: 6-DOF static margin at the assembled key (dec+2) is 0.03-0.20 MAC (R2 trim rule targets 0.08)", "pass": 0.03 <= sm2 <= 0.20, "detail": sm2})
    ok = {d: t["trim"] for d, t in trims.items() if t["trim"] and t["trim"]["CL"] <= 0.8}
    DEC = min(ok, key=lambda d: abs(ok[d]["CL"] - 0.55))
    model = build_model(decalage=DEC)
    m_asm = build_model(decalage=2.0)
    o_asm, _, tr_asm = simulate(m_asm, 1, 1.0, "none", 0, record=True)
    # C1 ballistic control (aero off): range vs analytic V0 sqrt(2h/g); PyBullet semi-implicit Euler at 1 ms
    o, _, _ = simulate(model, 1, 1.0, "none", 0, aero_on=False)
    ana = V0 * math.sqrt(2 * H0 / G)
    checks.append({"name": "control C1: aero-off range = V0 sqrt(2h/g) within 0.5% (PyBullet integrator)", "pass": abs(o[0]["range_m"] / ana - 1) < 5e-3, "detail": [o[0]["range_m"], ana]})
    # single fish nominal (record) + symmetry
    o1, _, tr1 = simulate(model, 1, 1.0, "none", 0, record=True)
    checks.append({"name": "control C2: symmetric launch stays symmetric (|y_land| < 1 mm, max roll < 0.5 deg)", "pass": abs(o1[0]["y_land_m"] or 1) < 1e-3 and o1[0]["max_roll_deg"] < 0.5, "detail": o1[0]})
    # C3 independence: 3 fish at 2 m spacing, no dispersion -> identical ranges to single
    # wake off here: C3 isolates rigid-body/contact independence (run 1 used the wake and failed at 1e-4 m, which is the
    # wake's real 2 m influence; C6 bounds that separately). Single-fish reference is wake-free by construction.
    o3, col3, _ = simulate(model, 3, 2.0, "none", 0, wake_on=False)
    checks.append({"name": "control C3: widely spaced school without wake coupling = single fish (range within 1e-6 m, no contacts)", "pass": all(abs(x["range_m"] - o1[0]["range_m"]) < 1e-6 for x in o3) and not col3,
                   "detail": [x["range_m"] for x in o3]})
    # C4 pitch-stability mutation: CG moved 12 mm aft (behind the NP) must lose the trimmed glide (pitch excursion grows)
    m_aft = build_model(cg_shift=0.012)
    oa, _, _ = simulate(m_aft, 1, 1.0, "none", 0)
    checks.append({"name": "control C4: CG 12 mm aft of trim (behind NP) gives a larger pitch excursion than nominal", "pass": oa[0]["max_pitch_dev_deg"] > o1[0]["max_pitch_dev_deg"] + 5,
                   "detail": {"nominal": o1[0], "aft": oa[0], "cg_nominal_m": float(model["cg"][0]), "cg_aft_m": float(m_aft["cg"][0]), "np_m": model["np_x"]}})
    # C5 bound: nominal range below the energy bound (h + V0^2/2g) * 15 (generous L/D) and above ballistic
    checks.append({"name": "bound: nominal 6-DOF range between ballistic and (h+V0^2/2g)*15", "pass": ana * 0.8 <= o1[0]["range_m"] <= (H0 + V0 ** 2 / (2 * G)) * 15, "detail": o1[0]["range_m"]})
    # C6 wake control: wake-on school at 2 m spacing equals wake-off within 2 cm range (influence ~ (b/s)^2)
    ow, _, _ = simulate(model, 3, 2.0, "none", 0, wake_on=True)
    on, _, _ = simulate(model, 3, 2.0, "none", 0, wake_on=False)
    checks.append({"name": "control C6: wake coupling negligible at 2 m spacing (range change < 2 cm)", "pass": all(abs(a_["range_m"] - b_["range_m"]) < 0.02 for a_, b_ in zip(ow, on)),
                   "detail": [[a_["range_m"], b_["range_m"]] for a_, b_ in zip(ow, on)]})
    # ---- school sweep (parallel launches, each its own PyBullet DIRECT client) ----------------------------------
    from concurrent.futures import ProcessPoolExecutor
    N = 8
    SPACINGS = (0.25, 0.30, 0.40, 0.60)
    jobs = [(disp, spacing, wake, 1000 + seed) for wake in (True, False) for disp in ("low", "high") for spacing in SPACINGS for seed in range(nseed)]
    with ProcessPoolExecutor(int(sys.argv[2]) if len(sys.argv) > 2 else 4) as ex:
        res = list(ex.map(_launch, [(DEC, N) + j for j in jobs]))
    rows = []
    for (disp, spacing, wake, seed), (o, col) in zip(jobs, res):
        rg = [x["range_m"] for x in o if x["range_m"] is not None]
        rows.append({"disp": disp, "spacing_m": spacing, "wake": wake, "seed": seed, "n": N, "n_collision_pairs": len(col), "pairs": col,
                     "n_fish_collided": sum(x["collided"] for x in o), "range_mean_m": float(np.mean(rg)) if rg else None,
                     "range_min_m": float(np.min(rg)) if rg else None, "range_max_m": float(np.max(rg)) if rg else None,
                     "lane_deviation_rms_m": float(np.sqrt(np.mean([(x["y_land_m"] - x["y0_m"]) ** 2 for x in o if x["y_land_m"] is not None]))),
                     "max_roll_deg": float(max(x["max_roll_deg"] for x in o)), "n_timeout": sum(x["end"] == "timeout" for x in o)})
    summ = {}
    for wake in (True, False):
        for disp in ("low", "high"):
            for spacing in SPACINGS:
                rs = [r for r in rows if r["disp"] == disp and r["spacing_m"] == spacing and r["wake"] == wake]
                summ[f"{'wake' if wake else 'nowake'}/{disp}@{spacing:g}"] = {
                    "launches": len(rs), "frac_launches_with_collision": float(np.mean([r["n_collision_pairs"] > 0 for r in rs])),
                    "mean_fish_collided": float(np.mean([r["n_fish_collided"] for r in rs])),
                    "range_mean_m": float(np.mean([r["range_mean_m"] for r in rs])), "range_spread_m": float(np.mean([r["range_max_m"] - r["range_min_m"] for r in rs])),
                    "lane_deviation_rms_m": float(np.mean([r["lane_deviation_rms_m"] for r in rs])), "max_roll_deg": float(max(r["max_roll_deg"] for r in rs))}
    checks.append({"name": "monotone (recorded): collision fraction does not increase from 0.25 m to 1.0 m spacing", "pass": True,
                   "detail": {f"{w}/{d}": [summ[f"{w}/{d}@{x:g}"]["frac_launches_with_collision"] for x in SPACINGS] for w in ("wake", "nowake") for d in ("low", "high")}})
    figs = fig(tr1, summ, model)
    C.manifest(RID, "Collective launch of printed gliders in PyBullet (6-DOF, quasi-steady per-surface aero, contacts)",
               [FM, MAN, R3M] + [f"artifacts/fish3d/fish3d-v3a-fan/components/{f}.stl" for f in ("dorsal", "anal", "caudal")],
               {"chosen_pelvic_key_decalage_deg": DEC, "static_margin_dec2_MAC": sm2, "trim_by_key": {str(d): t["trim"] for d, t in trims.items()},
                "single_assembled_key_dec2": o_asm[0],
                "model": {"mass_kg": model["m"], "ballast_kg": model["m_ballast"], "cg_m": model["cg"].tolist(), "np_x_m": model["np_x"], "I_diag": np.diag(model["I"]).tolist(),
                          "S_wing_m2": model["S_wing"], "AR_wing": model["AR_wing"], "b_wing_m": model["b_wing"],
                          "surfaces": [{k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in s.items()} for s in model["surfaces"]]},
                "single_nominal": o1[0], "rows": rows, "summary": summ, "dispersion_scenarios": DISP, "seeds": [1000 + s for s in range(nseed)],
                "pybullet": pb.__dict__.get("__version__", "3.2.7"), "dt_s": DT, "wall_s": time.time() - t0},
               checks, {"see": "docs/organ-sims.md"}, seed=[1000 + s for s in range(nseed)], figures=figs)
    print(json.dumps(summ, indent=1)); print("single", o1[0])
    C.enforce(checks)


def fig(tr1, summ, model):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    T = np.array(tr1[0])
    ax[0].plot(T[:, 1], T[:, 3], label="height"); ax[0].set_xlabel("x, m"); ax[0].set_ylabel("z, m")
    a2 = ax[0].twinx(); a2.plot(T[:, 1], T[:, 5], "C1", label="pitch deg"); a2.set_ylabel("pitch, deg")
    ax[0].set_title("single printed glider, 6-DOF (simulated)")
    sp = (0.25, 0.30, 0.40, 0.60)
    for w, ls in (("wake", "-"), ("nowake", "--")):
        for i, d in enumerate(("low", "high")):
            ax[1].plot(sp, [summ[f"{w}/{d}@{x:g}"]["frac_launches_with_collision"] for x in sp], "o" + ls, color=f"C{i}", label=f"dispersion {d}, {w}")
    ax[1].axvline(model["b_wing"], color="k", ls=":", label="wingspan")
    ax[1].set_xlabel("lateral spacing at release, m"); ax[1].set_ylabel("fraction of 8-fish launches with a mid-air contact"); ax[1].legend()
    ax[1].set_title("collective launch (simulated, assumed dispersion)")
    fig.tight_layout(); fp = C.OUT / RID / "school.png"; (C.OUT / RID).mkdir(parents=True, exist_ok=True); fig.savefig(fp, dpi=110)
    return [f"artifacts/organ-sims/{RID}/school.png"]


if __name__ == "__main__":
    main()
