# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 20:14:40 2023

@author: dvezinet
"""


import itertools as itt


import numpy as np
import datastock as ds


# specific
from . import _class02_interpolate as _interpolate


# ############################################################
# ############################################################
#               interpolate spectral
# ############################################################


def binning(
    coll=None,
    keys=None,
    ref_key=None,
    bins=None,
):
    """ Return the spectrally interpolated coefs

    Either E xor Ebins can be provided
    - E: return interpolated coefs
    - Ebins: return binned (integrated) coefs
    """

    # ----------
    # checks

    # keys
    isbs, keys, ref_key, daxis, dunits, units_ref = _interpolate._check_keys(
        coll=coll,
        keys=keys,
        ref_key=ref_key,
        only1d=True,
    )

    # ----------
    # trivial

    if not isbs:
        return ds._class1_binning.binning(
            coll=coll,
            keys=keys,
            ref_key=ref_key[0],
            bins=bins,
        )

    # ---------
    # sampling

    # mesh knots
    keym = coll.dobj[coll._which_bsplines][ref_key][coll._which_mesh]
    kknots = coll.dobj[coll._which_mesh][keym]['knots'][0]

    # resolution
    vect = coll.ddata[kknots]['data']
    res0 = np.abs(np.min(np.diff(vect)))

    # ----------
    # bins

    # bins
    bins, units_bins, db, npts = ds._class1_binning._check_bins(
        coll=coll,
        keys=keys,
        ref_key=ref_key,
        bins=bins,
        vect=vect,
        strict=False,
        deg=coll.dobj[coll._which_bsplines][ref_key]['deg'],
    )

    # sample mesh
    xx = coll.get_sample_mesh(keym, res=res0 / npts, mode='abs')

    # units
    dout = ds._class1_binning._units(
        dunits=dunits,
        units_ref=units_ref,
        units_bins=units_bins,
    )

    # --------------
    # actual binning

    for k0, v0 in dout.items():

        # interpolate
        val = coll.interpolate(
            keys=k0,
            ref_key=ref_key,
            x0=xx,
            val_out=0.,
        )[k0]['data']

        # bin
        dout[k0]['data'] = ds._class1_binning._bin(
            bins=bins,
            db=db,
            vect=xx,
            data=val,
            axis=daxis[k0][0],
        )
        ref = list(coll.ddata[k0]['ref'])
        ref[daxis[k0][0]] = None
        dout[k0]['ref'] = tuple(ref)

    return dout
