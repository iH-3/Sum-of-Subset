#!/usr/bin/env python3
"""Exact scalar replay for the fresh high-hole localization proof."""
from pathlib import Path
import json


def T(r):
    return r * (r + 1) // 2


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parents[2]
    source = root / 'audit/verification_program/foundations/dense/data/profiles.json'
    rows = json.loads(source.read_text())
    profiles = {(r['h'], r['r']): r for r in rows}
    expected_mu = {15: 426, 17: 470, 21: 514, 49: 554}
    expected_rho = {15: 294, 17: 338, 21: 382, 49: 422}
    minima = {}
    for h in expected_mu:
        pairs = [(profiles[h, a]['mu'] + profiles[h, 68-a]['mu'],
                  profiles[h, a]['elementary_rho'] +
                  profiles[h, 68-a]['elementary_rho'])
                 for a in range(15, 54)]
        mu = min(x[0] for x in pairs)
        rho = min(x[1] for x in pairs)
        require((mu, rho) == (expected_mu[h], expected_rho[h]), 'profile floor')
        minima[h] = {'mu': mu, 'rho': rho, 'orientations': len(pairs)}

    require(1 + 12 + (2 * 75 + 3) == 166, 'two-maximum envelope')
    require(1190 + 612 - 292 == 1510, 'offset-sum constant')
    require(72 + 1510 // 2 == 827, 'maximum constant')
    require(1190 - 827 - 2 * 600 == -837, 'width budget constant')

    bands = []
    for h, zmax, icap, hcap in [(15, 16, 194, 226),
                               (17, 20, 158, 198),
                               (21, 48, 170, 266)]:
        mu, rho = minima[h]['mu'], minima[h]['rho']
        require((mu + rho) % 2 == 0, 'integral scalar sum')
        width_margin = -837 + 3 * (mu + rho) // 2 - 3 * zmax
        kmax = max(k for k in range(20) if k*k <= icap)
        core_margin = min(T(34-k) - hcap + k*k for k in range(kmax+1))
        require(width_margin > 0 and core_margin > 0, 'strip applicability')
        bands.append(dict(h=h, width_margin=width_margin,
                          core_mass_margin=core_margin, kmax=kmax))
    require([b['width_margin'] for b in bands] == [195, 315, 363], 'width minima')
    require([b['core_mass_margin'] for b in bands] == [171, 199, 131], 'mass minima')
    tail_base = -837 + 3 * (554 + 422) // 2
    require(tail_base == 627 and tail_base - 3 * 178 == 93, 'tail width')
    tail_mass = min(T(34-k) - 356 + 2*k*k for k in range(12))
    require(tail_mass == 120, 'tail core mass')
    print(json.dumps(dict(status='PASS', profile_minima=minima,
                          bands=bands, tail_width_margin=93,
                          tail_core_mass_margin=tail_mass), indent=2))


if __name__ == '__main__':
    main()
