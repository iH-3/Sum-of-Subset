#!/usr/bin/env python3
"""Retained prefixes down to size 14; general proof in upper88 report."""
from nonap_sharp import require, nonap_floor
import retained_prefix as previous


def witness(r, rho_upper, depth=2):
    require(all(type(v) is int for v in (r,rho_upper,depth)), 'Integer parameters required')
    require(depth>=1 and r-depth>=14, 'Retained nonnegative prefix out of range')
    escape=(r-depth)*(r-depth+1)//2-r-1
    require(rho_upper<escape, 'Disjoint prefix step has not been excluded')
    return dict(size=r,depth=depth,rho_upper=rho_upper,escape=escape,
                surplus=escape-rho_upper,prefix_size=r-depth,
                rho_floor=nonap_floor(r-depth),mu_floor=r-depth-3,hole_denominator=2**depth)


def audit():
    out=previous.audit();checks=0
    for r in range(18,60):
        for depth in range(1,r-13):
            escape=(r-depth)*(r-depth+1)//2-r-1
            w=witness(r,escape-1,depth)
            require(w['surplus']==1,'Wrong strict escape threshold')
            if r-depth>=17:require(w==previous.witness(r,escape-1,depth),'Inherited witness changed')
            checks+=1
    return dict(previous=out,extended_parameter_checks=checks,minimum_prefix_size=14,
                scope='Exact parameter checks; extension uses the inherited nonnegative defect at size 14')
