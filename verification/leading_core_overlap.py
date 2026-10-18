"""Raw leading/own overlap and whole-side deficits for the size-89 model.

General proofs: reports/upper88_leading_overlap_20261018.tex.
These are necessary constraints, not by themselves an endpoint exclusion.
"""
import upper88_candidate as previous


def model(group, a, kind):
    names, rows = previous.model(group, a, kind)
    if kind != 'global_nested' or 'full_p' not in names:
        return names, rows
    slots = group['mode']['slots']
    whole = previous.row_policy(group)['fixed_scores']
    if whole:
        names = names + ['whole_p', 'whole_q']
        rows = {label: (vector + [0, 0], rhs)
                for label, (vector, rhs) in rows.items()}
    indices = {v: i for i, v in enumerate(names)}

    def row(label, coefficients, rhs):
        previous.require(label not in rows, 'Repeated row')
        vector = [0] * len(names)
        for key, value in coefficients.items():
            vector[indices[key]] = value
        rows[label] = vector, rhs

    for side in 'pq':
        baseline, _ = rows['full_' + side + '_sum']
        for slot in slots:
            if slot[0] != side or int(slot[1:]) >= 4:
                continue
            for keep in ('leading', 'own'):
                vector = baseline.copy()
                if keep == 'leading':
                    for end in ('l_', 'u_'):
                        vector[indices[end + slot]] = 0
                else:
                    vector[indices['lead_' + side]] = 0
                for key, value in {'Rp': -1, 'Rq': -1,
                                   side + str(int(slot[1:]) + 1): -1,
                                   'M' + side: 1}.items():
                    vector[indices[key]] += value
                rows['leading_core_' + slot + '_' + keep] = vector, -145
        if whole:
            members = [v for v in slots if v[0] == side]
            # The special modes have both paired units absent: every member
            # here is an unpaired physical translate on this same target.
            previous.require({'pair1', 'pair2'} <= set(group['mode']['missing']),
                             'Whole-side grouping includes a paired unit')
            individual = {end + v: 1 for v in members for end in ('l_', 'u_')}
            individual.update({'lead_' + side: 1, 'whole_' + side: -1})
            row('whole_' + side + '_individual', individual, 0)
            row('whole_' + side + '_target',
                {'K': 1, 'S' + side: -1, 'whole_' + side: -1},
                -81 * len(members))
            remainder = [v for v in members if v not in
                         [side + str(i) for i in (0, 1, 2, 3, 6, 7)]]
            linked = {end + v: 1 for v in remainder for end in ('l_', 'u_')}
            linked.update({'full_' + side: 1, 'whole_' + side: -1})
            row('whole_' + side + '_full', linked, 0)
    if whole:
        row('whole_joint', {'whole_p': 1, 'whole_q': 1, 'delta': -1,
                            'fixed_extra': 1},
            -previous.row_policy(group)['fixed_loss'])
    return names, rows


def branches(group, a, names):
    return previous.branches(group, a, names)
