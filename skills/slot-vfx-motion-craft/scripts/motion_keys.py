#!/usr/bin/env python3
r"""Keys and stagger tables for SlotVFX motion, from named eases and springs.

SlotVFX timeline keys with tangents {mode:"free", out:{dt,dv}, in:{dt,dv}}
evaluate exactly like a CSS / After Effects cubic-bezier between two keys, so
a named ease becomes two keys, and anything else (springs, log-space scale)
becomes a handful of fitted bezier keys.

  ease     two keys with handles for a named ease
           motion_keys.py ease --target image:banner --property scaleX \
               --from 0.2 --to 1 --start 0.3 --duration 0.45 --ease expo.out --log
  spring   a damped spring as fitted bezier keys (or --sampled linear keys)
           motion_keys.py spring --target image:banner --property y --from 380 --to 540 \
               --start 0.3 --response 0.45 --damping 0.6
           motion_keys.py spring ... --period 0.13 --decay 0.075   (spin-showcase landing)
  stagger  per-cell delays for a rows x cols board
           motion_keys.py stagger --rows 3 --cols 5 --origin center --amount 0.3
  chain    overlap and follow-through down a loose Spine chain (tail, hair, cape) from the
           lead bone's keys; not for spines or limbs that carry weight
           motion_keys.py chain --bones tail1,tail2,tail3,tail4 \
               --keys "0:0,0.25:-12,0.6:25:power2.out,1.0:0" --ease power2.inOut \
               --lag 0.1 --gain 1.2 --overshoot 0.15 [--loop 1.0] [--base tail1=-5,tail2=12,...]
  wave     a looping layer (breath, sway) on many Spine channels, each with its own amount,
           delay and period, wrapped exactly at the seam
           motion_keys.py wave --period 3.333 --shape breath \
               --channels "hip.y:1.2:0,chest.x:2.4:0.1,shoulder.x:1.4:0.167,neck.rotate:-0.5:0.2" \
               --base "hip.x=-11.97,hip.y=-23.15,neck.rotate=3.78"

--log interpolates in log space (for scale): equal ratios per frame instead of
equal steps, so a pop does not look like it stalls as it grows.
Key output is JSON: a list of batches of <= 180 keys for slotfx_set_timeline_keyframes
(timeMode "exact"). A summary goes to stderr.
"""
import argparse, json, math, random, sys

EASES = {  # cubic-bezier(x1, y1, x2, y2); GSAP names, easings.net curves
    'linear': (0, 0, 1, 1),
    'power1.in': (.11, 0, .5, 0), 'power1.out': (.5, 1, .89, 1), 'power1.inOut': (.45, 0, .55, 1),
    'power2.in': (.32, 0, .67, 0), 'power2.out': (.33, 1, .68, 1), 'power2.inOut': (.65, 0, .35, 1),
    'power3.in': (.5, 0, .75, 0), 'power3.out': (.25, 1, .5, 1), 'power3.inOut': (.76, 0, .24, 1),
    'power4.in': (.64, 0, .78, 0), 'power4.out': (.22, 1, .36, 1), 'power4.inOut': (.83, 0, .17, 1),
    'sine.in': (.12, 0, .39, 0), 'sine.out': (.61, 1, .88, 1), 'sine.inOut': (.37, 0, .63, 1),
    'expo.in': (.7, 0, .84, 0), 'expo.out': (.16, 1, .3, 1), 'expo.inOut': (.87, 0, .13, 1),
    'circ.in': (.55, 0, 1, .45), 'circ.out': (0, .55, .45, 1), 'circ.inOut': (.85, 0, .15, 1),
    'back.in': (.36, 0, .66, -.56), 'back.out': (.34, 1.56, .64, 1), 'back.inOut': (.68, -.6, .32, 1.6),
    # exhale: leaves the top of the breath gently, drops quickly, then settles slowly at the bottom
    'breath.out': (.3, 0, .2, 1),
}

def bezier_y(p, x):
    """CSS cubic-bezier: y for progress x."""
    x1, y1, x2, y2 = p
    bx = lambda s: 3 * x1 * s * (1 - s) ** 2 + 3 * x2 * s * s * (1 - s) + s ** 3
    lo, hi = 0.0, 1.0
    for _ in range(50):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if bx(m) < x else (lo, m)
    s = (lo + hi) / 2
    return 3 * y1 * s * (1 - s) ** 2 + 3 * y2 * s * s * (1 - s) + s ** 3

# ---------- fitting any f(t) on [0, T] with a few bezier keys ----------

def deriv(f, t, T):
    h = 1e-5
    a, b = max(0.0, t - h), min(T, t + h)
    return (f(b) - f(a)) / (b - a)

def fit_segment(f, t0, t1, T):
    """Handles matching the end slopes; lengths chosen to minimise max error."""
    d = t1 - t0; s0, s1 = deriv(f, t0, T), deriv(f, t1, T)
    v0, v1 = f(t0), f(t1)
    probe = [t0 + d * k / 16 for k in range(1, 16)]
    want = [f(t) for t in probe]
    best = None
    for i in range(3, 70, 3):
        for j in range(3, 70, 3):
            a, b = d * i / 100, d * j / 100
            P = ((t0, v0), (t0 + a, v0 + s0 * a), (t1 - b, v1 - s1 * b), (t1, v1))
            err = 0.0
            for t, w in zip(probe, want):
                lo, hi = 0.0, 1.0
                for _ in range(30):
                    m = (lo + hi) / 2
                    x = (1-m)**3*P[0][0] + 3*m*(1-m)**2*P[1][0] + 3*m*m*(1-m)*P[2][0] + m**3*P[3][0]
                    lo, hi = (m, hi) if x < t else (lo, m)
                m = (lo + hi) / 2
                y = (1-m)**3*P[0][1] + 3*m*(1-m)**2*P[1][1] + 3*m*m*(1-m)*P[2][1] + m**3*P[3][1]
                err = max(err, abs(y - w))
                if best and err >= best[0]: break
            if best is None or err < best[0]:
                best = (err, (a, s0 * a), (-b, -s1 * b))
    return best

def fit_keys(f, T, ts, tol):
    ts = sorted(set(round(t, 9) for t in ts + [0.0, T]))
    for _ in range(7):
        out, split = [ts[0]], False
        for t0, t1 in zip(ts, ts[1:]):
            if fit_segment(f, t0, t1, T)[0] > tol:
                out.append((t0 + t1) / 2); split = True
            out.append(t1)
        ts = out
        if not split: break
    keys, worst, pending_in = [], 0.0, None
    for i, t in enumerate(ts):
        tang = {"mode": "free"}
        if pending_in: tang["in"] = pending_in
        if i + 1 < len(ts):
            err, o, n = fit_segment(f, t, ts[i + 1], T)
            worst = max(worst, err)
            tang["out"] = {"dt": round(o[0], 6), "dv": round(o[1], 5)}
            pending_in = {"dt": round(n[0], 6), "dv": round(n[1], 5)}
        keys.append((t, f(t), tang))
    return keys, worst

# ---------- springs ----------

def spring_fn(w, z, x0, v0):
    """Displacement from the target at time t (closed form, no state)."""
    if z < 1:
        wd = w * math.sqrt(1 - z * z); B = (v0 + z * w * x0) / wd
        return lambda t: math.exp(-z * w * t) * (x0 * math.cos(wd * t) + B * math.sin(wd * t))
    if z == 1:
        B = v0 + w * x0
        return lambda t: math.exp(-w * t) * (x0 + B * t)
    r1, r2 = -w * (z - math.sqrt(z * z - 1)), -w * (z + math.sqrt(z * z - 1))
    C2 = (v0 - r1 * x0) / (r2 - r1); C1 = x0 - C2
    return lambda t: C1 * math.exp(r1 * t) + C2 * math.exp(r2 * t)

def emit(a, keys, note):
    rows = [{"targetId": a.target, "property": a.property, "time": round(a.start + t, 6),
             "timeMode": "exact", "value": round(v, 5), "tangents": tang} for t, v, tang in keys]
    print(note, file=sys.stderr)
    json.dump([rows[i:i + 180] for i in range(0, len(rows), 180)], sys.stdout)
    print()

def cmd_ease(a):
    p = EASES[a.ease]; D = a.duration
    if not a.log:
        dv = a.to - a.frm
        keys = [(0.0, a.frm, {"mode": "free", "out": {"dt": round(p[0] * D, 6), "dv": round(p[1] * dv, 5)}}),
                (D, a.to, {"mode": "free", "in": {"dt": round((p[2] - 1) * D, 6), "dv": round((p[3] - 1) * dv, 5)}})]
        return emit(a, keys, f"{a.ease}: 2 keys, exact")
    if a.frm <= 0 or a.to <= 0: sys.exit('--log needs positive --from and --to (scale)')
    r = a.to / a.frm
    f = lambda t: a.frm * r ** bezier_y(p, min(1.0, max(0.0, t / D)))
    tol = a.fit_tol if a.fit_tol is not None else 0.002 * abs(a.to - a.frm)
    keys, worst = fit_keys(f, D, [], tol)
    keys[-1] = (D, a.to, keys[-1][2])
    emit(a, keys, f"{a.ease} in log space: {len(keys)} keys, worst fit error {worst:.4g}")

def cmd_spring(a):
    if a.response:
        w, z = 2 * math.pi / a.response, a.damping
    elif a.period and a.decay:
        wd, zw = 2 * math.pi / a.period, 1 / a.decay
        w = math.hypot(wd, zw); z = zw / w
    else:
        sys.exit('give --response (with --damping) or --period with --decay')
    if a.log:
        if a.frm <= 0 or a.to <= 0: sys.exit('--log needs positive values')
        L0, L1 = math.log(a.frm), math.log(a.to)
        x = spring_fn(w, z, L0 - L1, a.v0 / a.frm)
        f = lambda t: math.exp(L1 + x(t))
    else:
        x = spring_fn(w, z, a.frm - a.to, a.v0)
        f = lambda t: a.to + x(t)
    span = abs(a.to - a.frm) or abs(a.v0) / w
    eps = a.settle if a.settle is not None else 0.002 * span
    T, t = 0.0, 0.0
    while t < 10:
        if abs(f(t) - a.to) > eps: T = t
        t += 1 / 2000
    T += 1 / 2000
    sgn = 1 if a.to >= a.frm else -1
    peak = max((f(k / 2000) - a.to) * sgn for k in range(int(T * 2000) + 1))
    over = f"overshoot {max(peak, 0):.4g}" + (f" ({100 * max(peak, 0) / span:.1f}% of travel)" if a.to != a.frm else "")
    head = f"damping ratio {z:.3f}, response {2 * math.pi / w:.3f}s, settles in {T:.3f}s, {over}"
    if a.sampled:
        n = math.ceil(T * a.fps)
        keys = [(min(i / a.fps, T), a.to if i == n else f(i / a.fps), {"mode": "linear"}) for i in range(n + 1)]
        return emit(a, keys, head + f"; {len(keys)} linear keys at {a.fps:g} fps")
    ts, prev, step = [], None, 1 / 4000
    for k in range(1, int(T / step)):           # peaks, troughs and target crossings
        t = k * step; d = f(t + step) - f(t)
        if prev is not None and prev * d < 0: ts.append(t)
        if (f(t) - a.to) * (f(t + step) - a.to) < 0: ts.append(t + step / 2)
        prev = d
    tol = a.fit_tol if a.fit_tol is not None else 0.0025 * span
    keys, worst = fit_keys(f, T, ts, tol)
    keys[-1] = (T, a.to, keys[-1][2])
    emit(a, keys, head + f"; {len(keys)} bezier keys, worst fit error {worst:.4g}")

def cmd_stagger(a):
    R, C = a.rows, a.cols
    cells = [(r, c) for r in range(R) for c in range(C)]
    if a.origin == 'center':   d = {rc: math.hypot(rc[0] - (R - 1) / 2, rc[1] - (C - 1) / 2) for rc in cells}
    elif a.origin == 'edges':
        m = {rc: math.hypot(rc[0] - (R - 1) / 2, rc[1] - (C - 1) / 2) for rc in cells}
        top = max(m.values()); d = {rc: top - v for rc, v in m.items()}
    elif a.origin == 'start':  d = {rc: math.hypot(*rc) for rc in cells}
    elif a.origin == 'end':    d = {rc: math.hypot(R - 1 - rc[0], C - 1 - rc[1]) for rc in cells}
    elif a.origin == 'reels':  d = {rc: rc[1] for rc in cells}
    elif a.origin == 'random':
        rnd = random.Random(a.seed); order = cells[:]; rnd.shuffle(order)
        d = {rc: i for i, rc in enumerate(order)}
    elif a.origin.startswith('line:'):          # payline: row index per column, e.g. line:1,0,0,0,1
        rows = [int(v) for v in a.origin[5:].split(',')]
        d = {(r, c): c for c, r in enumerate(rows)}
    else: sys.exit('origin: center|edges|start|end|reels|random|line:r,r,...')
    top = max(d.values()) or 1
    p = EASES[a.ease]
    delay = {}
    for rc, v in d.items():
        delay[rc] = round((a.amount * bezier_y(p, v / top)) if a.amount is not None else a.each * v, 4)
    for r in range(R):
        print('  '.join(f"{delay[(r, c)]:5.3f}" if (r, c) in delay else '   - ' for c in range(C)))
    print(json.dumps([{"row": r, "col": c, "delay": delay[(r, c)]} for (r, c) in sorted(delay)]))

def parse_chain_keys(text, default_ease):
    keys = []
    for part in text.split(','):
        bits = part.strip().split(':')
        if len(bits) not in (2, 3): sys.exit(f'bad key "{part}": use time:value or time:value:ease')
        ease = bits[2] if len(bits) == 3 else default_ease
        if ease not in EASES: sys.exit(f'unknown ease "{ease}"')
        keys.append([float(bits[0]), float(bits[1]), ease])
    keys.sort(key=lambda k: k[0])
    if len(keys) < 2: sys.exit('--keys needs at least two keys')
    return keys

def seg_points(t0, v0, t1, v1, ease):
    """Absolute bezier control points (t, v) for one segment with a named ease."""
    x1, y1, x2, y2 = EASES[ease]
    return [(t0, v0), (t0 + x1 * (t1 - t0), v0 + y1 * (v1 - v0)),
            (t0 + x2 * (t1 - t0), v0 + y2 * (v1 - v0)), (t1, v1)]

def split_points(P, t):
    """Split a bezier segment exactly at time t (de Casteljau at the matching parameter)."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        x = (1-m)**3*P[0][0] + 3*m*(1-m)**2*P[1][0] + 3*m*m*(1-m)*P[2][0] + m**3*P[3][0]
        lo, hi = (m, hi) if x < t else (lo, m)
    u = (lo + hi) / 2
    L = lambda a, b: (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
    a, b, c = L(P[0], P[1]), L(P[1], P[2]), L(P[2], P[3])
    d, e = L(a, b), L(b, c)
    f = L(d, e)
    return [P[0], a, d, f], [f, e, c, P[3]]

def spine_rows(ks, loop=None):
    """Spine rotate-style rows {time, value, curve:[cx1,cy1,cx2,cy2]} from [time, value, ease] keys.
    With loop L and keys running from some delay to delay + L, the cycle is rotated to start at 0
    and the segment that crosses the seam is split exactly."""
    segs = [seg_points(t0, v0, t1, v1, e0) if e0 != 'linear' else None
            for (t0, v0, e0), (t1, v1, _) in zip(ks, ks[1:])]
    if loop is not None and ks[0][0] % loop > 1e-9:
        L, shift = loop, ks[0][0] - ks[0][0] % loop
        pts = []
        for (t0, v0, e0), (t1, v1, _), P in zip(ks, ks[1:], segs):
            P = P or [(t0, v0), (t0, v0), (t1, v1), (t1, v1)]
            pts.append([(x - shift, y) for x, y in P])
        pieces = []
        for P in pts:
            if P[0][0] < L < P[3][0] - 1e-9:
                A, B = split_points(P, L)
                pieces += [A, B]
            else:
                pieces.append(P)
        pieces = [[((x - L) if P[0][0] >= L - 1e-9 else x, y) for x, y in P] for P in pieces]
        pieces.sort(key=lambda P: P[0][0])
        rows = [{"time": round(P[0][0], 5) + 0.0, "value": round(P[0][1], 4),
                 "curve": [round(c, 5 if i % 2 == 0 else 4) for pt in P[1:3] for i, c in enumerate(pt)]}
                for P in pieces]
        rows.append({"time": round(L, 5), "value": rows[0]["value"]})
        return rows
    rows = []
    for i, (t, v, e) in enumerate(ks):
        row = {"time": round(t, 5), "value": round(v, 4)}
        if i < len(segs) and segs[i]:
            row["curve"] = [round(c, 5 if j % 2 == 0 else 4) for pt in segs[i][1:3] for j, c in enumerate(pt)]
        rows.append(row)
    return rows

def cmd_chain(a):
    """Each level samples its parent `lag` seconds later and swings `gain` times as far.
    Rotate values are Spine timeline values (added to the setup pose)."""
    lead = parse_chain_keys(a.keys, a.ease)
    bones = [b.strip() for b in a.bones.split(',') if b.strip()]
    base = {}
    if a.base:
        parts = [p.strip() for p in a.base.split(',') if p.strip()]
        if all('=' in p for p in parts):
            base = {k.strip(): float(v) for k, v in (p.split('=', 1) for p in parts)}
            unknown = set(base) - set(bones)
            if unknown: sys.exit(f'--base names bones not in --bones: {", ".join(sorted(unknown))}')
        elif len(parts) == len(bones):
            base = dict(zip(bones, map(float, parts)))
        else:
            sys.exit('--base: give bone=angle pairs, or one angle per bone in --bones order')
    if a.loop is not None:
        if abs(lead[0][0]) > 1e-9 or abs(lead[-1][0] - a.loop) > 1e-6 or abs(lead[-1][1] - lead[0][1]) > 1e-6:
            sys.exit('--loop needs lead keys from 0 to the loop length, ending on the starting value')
        if a.overshoot: print('--overshoot is ignored in loops: the cycle already continues', file=sys.stderr)
    out = {}
    for level, bone in enumerate(bones):
        delay, scale = level * a.lag, a.gain ** level
        ks = [[t + delay, v * scale, e] for t, v, e in lead]
        if level and a.overshoot and a.loop is None:
            # follow-through: the child carries on past the end pose instead of stopping on it,
            # then swings back; the overshoot grows down the chain
            (tp, vp, _), (te, ve, ee) = ks[-2], ks[-1]
            ks[-1] = [te, ve + (ve - vp) * a.overshoot * level, 'sine.inOut']
            ks.append([te + a.lag * 2.5, ve, ee])
        rows = spine_rows(ks, a.loop)
        b = base.get(bone, 0.0)
        if b:
            for row in rows:
                row["value"] = round(row["value"] + b, 4)
                if "curve" in row:
                    row["curve"][1] = round(row["curve"][1] + b, 4)
                    row["curve"][3] = round(row["curve"][3] + b, 4)
        out[bone] = {"rotate": rows}
        print(f"{bone}: delay {delay:.3f}s, x{scale:.2f}, {len(rows)} keys", file=sys.stderr)
    print(json.dumps({"bones": out}, separators=(',', ':')).replace('{"time"', '\n  {"time"'))

SHAPES = {  # one cycle on [0, 1]: (phase, value 0..1, ease of the segment that starts there)
    'breath': lambda r: [(0.0, 0.0, 'sine.inOut'), (r, 1.0, 'breath.out'), (1.0, 0.0, None)],
    'sine': lambda r: [(0.0, 0.0, 'sine.inOut'), (0.5, 1.0, 'sine.inOut'), (1.0, 0.0, None)],
}
CHANNELS = {'rotate': ('rotate', 'value'), 'x': ('translate', 'x'), 'y': ('translate', 'y'),
            'scaleX': ('scale', 'x'), 'scaleY': ('scale', 'y')}

def cmd_wave(a):
    """Each channel = base + amount * shape(time - delay), looping every --period * --cycles seconds.
    Values are Spine timeline values: rotate and translate are added to the setup pose, scale multiplies it."""
    L = a.period * a.cycles
    base = {}
    for part in filter(None, (p.strip() for p in (a.base or '').split(','))):
        k, v = part.split('=', 1); base[k.strip()] = float(v)
    chans = {}
    for part in filter(None, (p.strip() for p in a.channels.split(','))):
        bits = part.split(':')
        if len(bits) < 2 or '.' not in bits[0]: sys.exit(f'bad channel "{part}": use bone.channel:amount[:delay[:period]]')
        bone, ch = bits[0].rsplit('.', 1)
        if ch not in CHANNELS: sys.exit(f'channel "{ch}": use rotate, x, y, scaleX or scaleY')
        amt = float(bits[1]); delay = float(bits[2]) if len(bits) > 2 else 0.0
        per = float(bits[3]) if len(bits) > 3 else a.period
        n = L / per
        if abs(n - round(n)) > 1e-6: sys.exit(f'{part}: its period {per} must fit a whole number of times into the loop {L}')
        rest = base.get(f'{bone}.{ch}', 1.0 if ch.startswith('scale') else 0.0)
        ks = []
        for c in range(int(round(n))):
            for ph, v, e in SHAPES[a.shape](a.rise):
                if ks and ph == 0.0: continue
                ks.append([delay + (c + ph) * per, rest + amt * v, e or 'sine.inOut'])
        chans[(bone, ch)] = (spine_rows(ks, L), delay % L, per)
    out = {}
    for (bone, ch), (rows, delay, per) in chans.items():
        tl, fld = CHANNELS[ch]
        tls = out.setdefault(bone, {})
        if tl == 'rotate':
            tls['rotate'] = rows; continue
        other = 'y' if fld == 'x' else 'x'
        ochan = {'translate': {'x': 'x', 'y': 'y'}, 'scale': {'x': 'scaleX', 'y': 'scaleY'}}[tl][other]
        partner = chans.get((bone, ochan))
        if partner and (abs(partner[1] - delay) > 1e-9 or abs(partner[2] - per) > 1e-9):
            # different timing on x and y: Spine 4.x splits them into translatex/translatey or scalex/scaley
            tls[tl + fld] = rows
            if fld == 'x': print(f'{bone}: {tl} x and y have different timing, written as {tl}x / {tl}y timelines '
                                 '(give both the same delay and period to keep one timeline)', file=sys.stderr)
            continue
        merged = tls.setdefault(tl, [{"time": r["time"]} for r in rows])
        orest = base.get(f'{bone}.{ochan}', 1.0 if tl == 'scale' else 0.0)
        for m, r in zip(merged, rows):
            m[fld] = r["value"]
            m.setdefault(other, orest)
            if "curve" in r:
                cur = m.setdefault("curve", [None] * 8)
                o = 0 if fld == 'x' else 4
                cur[o:o + 4] = r["curve"]
    for tls in out.values():
        for tl in ('translate', 'scale'):
            rows = tls.get(tl, [])
            for m, nxt in zip(rows, rows[1:]):
                if "curve" in m and None in m["curve"]:
                    o = 0 if m["curve"][0] is None else 4      # the constant partner: flat handles on its value
                    v = m['x' if o == 0 else 'y']; t0, t1 = m["time"], nxt["time"]
                    m["curve"][o:o + 4] = [round(t0 + (t1 - t0) / 3, 5), v, round(t0 + 2 * (t1 - t0) / 3, 5), v]
    for (bone, ch), (rows, delay, per) in sorted(chans.items()):
        vals = [r["value"] for r in rows]
        print(f'{bone}.{ch}: delay {delay:.3f}s, period {per:g}s, {min(vals):.4g}..{max(vals):.4g}, {len(rows)} keys', file=sys.stderr)
    print(json.dumps({"bones": out}, separators=(',', ':')).replace('{"time"', '\n  {"time"'))

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    for name in ('ease', 'spring'):
        s = sub.add_parser(name)
        s.add_argument('--target', required=True); s.add_argument('--property', required=True)
        s.add_argument('--from', dest='frm', type=float, required=True); s.add_argument('--to', type=float, required=True)
        s.add_argument('--start', type=float, default=0.0)
        s.add_argument('--log', action='store_true', help='interpolate in log space (scale)')
        s.add_argument('--fit-tol', type=float, help='max fit error per segment, value units')
    se = sub.choices['ease']
    se.add_argument('--duration', type=float, required=True)
    se.add_argument('--ease', choices=sorted(EASES), default='power3.out')
    ss = sub.choices['spring']
    ss.add_argument('--response', type=float, help='seconds per undamped oscillation')
    ss.add_argument('--damping', type=float, default=1.0, help='damping ratio, 1 = no overshoot')
    ss.add_argument('--period', type=float, help='seconds per visible wobble (alternative form)')
    ss.add_argument('--decay', type=float, help='decay time constant in seconds (alternative form)')
    ss.add_argument('--v0', type=float, default=0.0, help='starting velocity, value units/s')
    ss.add_argument('--settle', type=float, help='settled when within this many value units')
    ss.add_argument('--sampled', action='store_true', help='linear keys every 1/fps instead of bezier keys')
    ss.add_argument('--fps', type=float, default=60.0)
    st = sub.add_parser('stagger')
    st.add_argument('--rows', type=int, required=True); st.add_argument('--cols', type=int, required=True)
    st.add_argument('--origin', default='center')
    st.add_argument('--amount', type=float, help='total spread in seconds (first to last)')
    st.add_argument('--each', type=float, help='or seconds per unit of distance')
    st.add_argument('--ease', choices=sorted(EASES), default='linear', help='shape of the spread')
    st.add_argument('--seed', type=int, default=1)
    sc = sub.add_parser('chain', help='overlap down a bone chain')
    sc.add_argument('--bones', required=True, help='lead bone first, e.g. hip,tail1,tail2')
    sc.add_argument('--keys', required=True, help='lead bone rotate keys: time:value[:ease of the segment starting here],...')
    sc.add_argument('--ease', choices=sorted(EASES), default='power2.inOut', help='default ease per segment')
    sc.add_argument('--lag', type=float, default=0.1, help='seconds each level lags its parent (2-4 frames)')
    sc.add_argument('--gain', type=float, default=1.15, help='rotation multiplier per level')
    sc.add_argument('--overshoot', type=float, default=0.0, help='follow-through past the final pose, fraction per level')
    sc.add_argument('--base', help="each bone's resting rotate value, added to its keys: "
                    "bone=angle,... or one angle per bone (e.g. the idle's first pose); "
                    "write --base=-22.9,3.8 when the list starts with a minus")
    sc.add_argument('--loop', type=float, help='cycle length: wrap delayed keys around the seam exactly, so the cycle stays seamless')
    sw = sub.add_parser('wave', help='looping breath or sway layer on many channels')
    sw.add_argument('--period', type=float, required=True, help='seconds per cycle (a breath: 2-4 s in games)')
    sw.add_argument('--cycles', type=int, default=1, help='cycles per loop; the loop is period x cycles')
    sw.add_argument('--shape', choices=sorted(SHAPES), default='breath',
                    help='breath: slower inhale, quicker exhale, settle at the bottom; sine: even sway')
    sw.add_argument('--rise', type=float, default=0.4, help='breath: share of the cycle spent inhaling')
    sw.add_argument('--channels', required=True,
                    help='bone.channel:amount[:delay[:period]],... channel = rotate|x|y|scaleX|scaleY; '
                         'amount is the peak offset from the base; delay in seconds; period must divide the loop')
    sw.add_argument('--base', help="bone.channel=value,... each channel's resting value (e.g. the idle's first pose); "
                    'unset channels rest at 0 (scale at 1)')
    a = p.parse_args()
    if a.cmd == 'stagger' and (a.amount is None) == (a.each is None):
        p.error('stagger needs exactly one of --amount or --each')
    {'ease': cmd_ease, 'spring': cmd_spring, 'stagger': cmd_stagger, 'chain': cmd_chain, 'wave': cmd_wave}[a.cmd](a)

if __name__ == '__main__':
    main()
