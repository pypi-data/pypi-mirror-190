# -*- coding: utf-8 -*-


# Built-in
import warnings


# Common
import numpy as np
from matplotlib.tri import Triangulation as mplTri
import datastock as ds


_ELEMENTS = 'knots'


# #############################################################################
# #############################################################################
#               mesh vs bsplines
# #############################################################################


def _get_key_mesh_vs_bplines(
    coll=None,
    key=None,
    forcecat=None,
    which_mesh=None,
    which_bsplines=None,
):


    if forcecat in [None, 'mesh'] and which_mesh in [None, coll._which_mesh]:
        lk1 = list(coll.dobj.get(coll._which_mesh, {}).keys())
    else:
        lk1 = []

    if forcecat in [None, 'mesh'] and which_mesh in [None, coll._which_msp]:
        lk2 = list(coll.dobj.get(coll._which_msp, {}).keys())
    else:
        lk2 = []

    if forcecat in [None, 'bsplines'] and which_bsplines in [None, 'bsplines']:
        lk3 = list(coll.dobj.get('bsplines', {}).keys())
    else:
        lk3 = []

    if forcecat in [None, 'bsplines'] and which_bsplines in [None, coll._which_bssp]:
        lk4 = list(coll.dobj.get(coll._which_bssp, {}).keys())
    else:
        lk4 = []

    # key
    key = ds._generic_check._check_var(
        key, 'key',
        allowed=lk1 + lk2 + lk3 + lk4,
        types=str,
    )

    # which
    if key in lk1 + lk3:
        which_mesh = coll._which_mesh
        which_bsplines = 'bsplines'
    else:
        which_mesh = coll._which_msp
        which_bsplines = coll._which_bssp

    # mesh vs bsplines
    if key in lk1 + lk2:
        cat = which_mesh
    else:
        cat = which_bsplines

    # keys
    if cat == which_mesh:
        keym = key
        keybs = None
    else:
        keym = coll.dobj[which_bsplines][key][which_mesh]
        keybs = key

    return which_mesh, which_bsplines, keym, keybs, cat


# #############################################################################
# #############################################################################
#                           mesh generic check
# #############################################################################


def _mesh2D_check(
    coll=None,
    domain=None,
    res=None,
    R=None,
    Z=None,
    knots=None,
    cents=None,
    trifind=None,
    key=None,
):

    # key
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=list(coll.dobj.get('mesh', {}).keys())
    )

    # rect of tri ?
    lc = [
        domain is not None or (R is not None and Z is not None),
        knots is not None and cents is not None,
    ]
    if all(lc) or not any(lc):
        msg = (
            "Either domain xor (R, Z) xor (knots, cents) must be provided!\n"
            "Provided:\n"
            f"\t- domain, res: {domain}, {res}\n"
            f"\t- type(R), type(Z): {type(R)}, {type(Z)}\n"
            f"\t- type(knots), type(cents): {type(knots)}, {type(cents)}\n"
        )
        raise Exception(msg)

    elif lc[0]:
        dref, ddata, dmesh = _mesh2DRect_to_dict(
            domain=domain,
            res=res,
            R=R,
            Z=Z,
            key=key,
        )

    elif lc[1]:
        dref, ddata, dmesh = _mesh2DTri_to_dict(
            knots=knots,
            cents=cents,
            trifind=trifind,
            key=key,
        )

    return dref, ddata, dmesh


def _mesh2D_polar_check(
    coll=None,
    radius=None,
    angle=None,
    radius2d=None,
    angle2d=None,
    key=None,
    # parameters
    radius_dim=None,
    radius_quant=None,
    radius_name=None,
    radius_units=None,
    angle_dim=None,
    angle_quant=None,
    angle_name=None,
):

    # key
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        excluded=list(coll.dobj.get('mesh', {}).keys())
    )

    # --------------------
    # check / format input

    krk, krc, kkr, kcr = _mesh_names(key=key, x_name='r')
    kak, kac, kka, kca = _mesh_names(key=key, x_name='ang')

    # radius data
    radius, _, _ = _mesh1D_check(
        x=radius,
        x_name='radius',
        uniform=False,
    )

    # angle data
    c0 = (
        angle is None
        or (
            hasattr(angle, '__iter__')
            and np.asarray(angle).ndim == 1
            and np.unique(angle).size == np.array(angle).size
            and np.allclose(
                np.unique(np.arctan2(np.sin(angle), np.cos(angle))),
                angle,
            )
        )
    )
    if not c0:
        msg = (
            "Arg angle either\n:"
            "\t- None: radial-only polar mesh"
            "\t- convertible to a 1d increasing array\n"
            "\t\t it must be in radians\n"
            "\t\t it must be in the [-pi; pi] interval\n"
            f"\t- Provided: {angle}"
        )
        raise Exception(msg)

    # extract data
    rknot = np.unique(radius)
    rcent = 0.5*(rknot[1:] + rknot[:-1])

    # radius2d
    dradius = _check_polar_2dquant(
        coll=coll,
        quant2d=radius2d,
        quant2d_name='radius2d',
        dim=radius_dim,
        quant=radius_quant,
        name=radius_name,
        units=radius_units,
    )

    if callable(radius2d):
        keysm = None
    else:
        keysm = coll.dobj['bsplines'][coll.ddata[radius2d]['bsplines']]['mesh']

    if angle is not None:
        aknot = np.unique(np.arctan2(np.sin(angle), np.cos(angle)))
        acent = 0.5*(aknot[1:] + aknot[:-1])
        amid = 0.5*(aknot[-1] + (2.*np.pi + aknot[0]))
        amid = np.arctan2(np.sin(amid), np.cos(amid))
        if amid < acent[0]:
            acent = np.r_[amid, acent]
        else:
            acent = np.r_[acent, amid]

    # -------
    # angle2d

    if angle2d is not None:
        dangle = _check_polar_2dquant(
            coll=coll,
            quant2d=angle2d,
            quant2d_name='angle2d',
            dim=angle_dim,
            quant=angle_quant,
            name=angle_name,
            units='rad',
        )

        # check angle units = rad
        if dangle['units'] != 'rad':
            msg = (
                "Angle units must be rad\n"
                f"\t Provided: {dangle['units']}"
            )
            raise Exception(msg)

        # check angle2d is like radius2d
        c0 = (
            (callable(radius2d) and callable(angle2d))
            or coll._ddata[radius2d]['ref'] == coll._ddata[angle2d]['ref']
        )
        if not c0:
            msg = (
                "radius2d and angle2d must be of the same type, either:\n"
                "\t- both callable\n"
                "\t- both data keys with identical ref!\n"
                f"Provided:\n"
                f"\t- radius2d: {radius2d}\n"
                f"\t- angle2d: {angle2d}\n"
            )
            raise Exception(msg)

    # --------------------
    # prepare dict

    # dref
    dref = {
        krk: {'size': rknot.size},
        krc: {'size': rcent.size},
    }

    if angle is not None:
        dref.update({
            kak: {
                'size': aknot.size,
            },
            kac: {
                'size': acent.size,
            },
        })

    # ddata
    ddata = {
        kkr: {
            'data': rknot,
            'ref': krk,
            **dradius,
        },
        kcr: {
            'data': rcent,
            'ref': krc,
            **dradius,
        },
    }

    if angle is not None:
        ddata.update({
            kka: {
                'data': aknot,
                'ref': kak,
                **dangle,
            },
            kca: {
                'data': acent,
                'ref': kac,
                **dangle,
            },
        })

    # dobj
    if angle is None:
        dmesh = {
            key: {
                'type': 'polar',
                'knots': (kkr,),
                'cents': (kcr,),
                'shape-c': rcent.shape,
                'shape-k': rknot.shape,
                'radius2d': radius2d,
                'angle2d': angle2d,
                'submesh': keysm,
                'crop': False,
            },
        }
    else:
        dmesh = {
            key: {
                'type': 'polar',
                'knots': (kkr, kka),
                'cents': (kcr, kca),
                'shape-c': (rcent.size, acent.size),
                'shape-k': (rknot.size, aknot.size),
                'radius2d': radius2d,
                'angle2d': angle2d,
                'submesh': keysm,
                'crop': False,
            },
        }

    return dref, ddata, dmesh


def _check_polar_2dquant(
    quant2d=None,
    coll=None,
    quant2d_name=None,
    # parameters
    dim=None,
    quant=None,
    name=None,
    units=None,
):

    if coll.dobj.get('bsplines') is not None:
        lok = [
            k0 for k0, v0 in coll.ddata.items()
            if v0.get('bsplines') in coll.dobj['bsplines'].keys()
        ]
    else:
        lok = []

    lc = [
        callable(quant2d),
        isinstance(quant2d, str) and quant2d in lok
    ]
    if not any(lc):
        msg = (
            f"Arg {quant2d_name} must be either:\n"
            f"\t- callable: {quant2d_name} = func(R, Z)\n"
            f"\t- key to existing 2d data in {lok}\n"
            f"Provided: {quant2d}\n"
        )
        raise Exception(msg)

    # quantities
    dquant = {'dim': dim, 'quant': quant, 'name': name, 'units': units}
    if isinstance(quant2d, str):
        for k0 in dquant.keys():
            if dquant[k0] is None:
                dquant[k0] = str(coll.ddata[quant2d][k0])

    return dquant


def _mesh_names(key=None, x_name=None):
    kxk, kxc = f'{key}-{x_name}-nk', f'{key}-{x_name}-nc'
    kkx, kcx = f'{key}-k-{x_name}', f'{key}-c-{x_name}'
    return kxk, kxc, kkx, kcx


# #############################################################################
# #############################################################################
#                           Mesh2DTri
# #############################################################################


def _mesh2DTri_conformity(knots=None, indices=None, key=None):

    # ---------------------------------
    # make sure np.ndarrays of dim = 2

    knots = np.atleast_2d(knots).astype(float)
    indices = np.atleast_2d(indices).astype(int)

    # --------------
    # check shapes

    c0 = (
        knots.shape[1] == 2
        and knots.shape[0] >= 3
        and indices.shape[1] in [3, 4]
        and indices.shape[0] >= 1
        and indices.dtype == int
    )
    if not c0:
        msg = (
            "Arg knots must be of shape (nknots>=3, 2) and "
            "arg cents must be of shape (nind>=1, 3 or 4) and dtype = int\n"
            "Provided:\n"
            f"\t- knots.shape: {knots.shape}\n"
            f"\t- indices.shape: {indices.shape}\n"
            f"\t- indices.dtype: {indices.dtype}\n"
        )
        raise Exception(msg)

    nknots = knots.shape[0]
    nind = indices.shape[0]

    # -------------------
    # Test for duplicates

    # knots (floats => distance)
    dist = np.full((nknots, nknots), np.nan)
    ind = np.zeros(dist.shape, dtype=bool)
    for ii in range(nknots):
        dist[ii, ii+1:] = np.sqrt(
            (knots[ii+1:, 0] - knots[ii, 0])**2
            + (knots[ii+1:, 1] - knots[ii, 1])**2
        )
        ind[ii, ii+1:] = True

    ind[ind] = dist[ind] < 1.e-6
    if np.any(ind):
        iind = np.any(ind, axis=1).nonzero()[0]
        lstr = [f'\t\t- {ii}: {ind[ii, :].nonzero()[0]}' for ii in iind]
        msg = (
            f"Non-valid mesh {key}: \n"
            f"  Duplicate knots: {ind.sum()}\n"
            f"\t- knots.shape: {indices.shape}\n"
            f"\t- duplicate indices:\n"
            + "\n".join(lstr)
        )
        raise Exception(msg)

    # cents (indices)
    indu = np.unique(indices, axis=0)
    if indu.shape[0] != nind:
        msg = (
            f"Non-valid mesh {key}: \n"
            f"  Duplicate cents: {nind - indu.shape[0]}\n"
            f"\t- indices.shape: {indices.shape}\n"
            f"\t- unique shape: {indu.shape}"
        )
        raise Exception(msg)

    # -------------------------------
    # Test for unused / unknown knots

    indu = np.unique(indu)
    c0 = np.all(indu >= 0) and indu.size == nknots

    # unused knots
    ino = (~np.in1d(
        range(0, nknots),
        indu,
        assume_unique=False,
        invert=False,
    )).nonzero()[0]

    # unknown knots
    unknown = np.setdiff1d(indu, range(nknots), assume_unique=True)

    if ino.size > 0 or unknown.size > 0:
        msg = "Knots non-conformity identified:\n"
        if ino.size > 0:
            msg += f"\t- Unused knots indices: {ino}\n"
        if unknown.size > 0:
            msg += f"\t- Unknown knots indices: {unknown}\n"
        raise Exception(msg)

    if indu.size < nknots:
        msg = (
            f"Unused knots in {key}:\n"
            f"\t- unused knots indices: {ino}"
        )
        warnings.warn(msg)

    elif indu.size > nknots or indu.max() != nknots - 1:
        unknown = np.setdiff1d(indu, range(nknots), assume_unique=True)
        msg = (
            "Unknown knots refered to in indices!\n"
            f"\t- unknown knots: {unknown}"
        )
        raise Exception(msg)

    return indices, knots


def _mesh2DTri_clockwise(knots=None, indices=None, key=None):

    x, y = knots[indices, 0], knots[indices, 1]
    orient = (
        (y[:, 1] - y[:, 0])*(x[:, 2] - x[:, 1])
        - (y[:, 2] - y[:, 1])*(x[:, 1] - x[:, 0])
    )

    clock = orient > 0.
    if np.any(clock):
        msg = (
            "Some triangles not counter-clockwise\n"
            "  (necessary for matplotlib.tri.Triangulation)\n"
            f"    => {clock.sum()}/{indices.shape[0]} triangles reshaped"
        )
        warnings.warn(msg)
        indices[clock, 1], indices[clock, 2] = indices[clock, 2], indices[clock, 1]
    return indices


def _mesh2DTri_to_dict(knots=None, indices=None, key=None, trifind=None):

    # ---------------------
    # check mesh conformity

    indices, knots = _mesh2DTri_conformity(knots=knots, indices=indices, key=key)

    # ---------------------------------------------
    # define triangular mesh and trifinder function

    # triangular mesh
    if indices.shape[1] == 3:

        # check clock-wise triangles
        indices = _mesh2DTri_clockwise(knots=knots, indices=indices, key=key)
        ntri = 1

    # Quadrangular mesh => convert to triangular
    elif indices.shape[1] == 4:

        ind2 = np.empty((indices.shape[0]*2, 3), dtype=int)
        ind2[::2, :] = indices[:, :3]
        ind2[1::2, :-1] = indices[:, 2:]
        ind2[1::2, -1] = indices[:, 0]
        indices = ind2

        # Re-check mesh conformity
        indices, knots = _mesh2DTri_conformity(knots=knots, indices=indices, key=key)
        indices = _mesh2DTri_clockwise(knots=knots, indices=indices, key=key)
        ntri = 2

    # check trifinder
    if trifind is None:
        trifind = mplTri(knots[:, 0], knots[:, 1], indices).get_trifinder()

    # ----------------------------
    # Check on trifinder function

    assert callable(trifind), "Arg trifind must be a callable!"

    try:
        out = trifind(np.r_[0.], np.r_[0])
        assert isinstance(out, np.ndarray)
    except Exception as err:
        msg = (
            "Arg trifind must return an array of indices when fed with arrays "
            "of (R, Z) coordinates!\n"
            f"\ttrifind(np.r_[0], np.r_[0.]) = {out}"
        )
        raise Exception(msg)

    # -----------------
    # Format ouput dict

    kk = f"{key}_nk"
    kc = f"{key}_nc"
    ki = f"{key}_nind"

    _, _, kkR, kcR = _mesh_names(key=key, x_name='x0')
    _, _, kkZ, kcZ = _mesh_names(key=key, x_name='x1')

    kii = f"{key}_ind"

    # dref
    dref = {
        kk: {
            'size': knots.shape[0],
        },
        kc: {
            'size': indices.shape[0],
        },
        ki: {
            'size': 3,
        },
    }

    # ddata
    ddata = {
        kkR: {
            'data': knots[:, 0],
            'units': 'm',
            'quant': 'R',
            'dim': 'distance',
            'ref': kk,
        },
        kkZ: {
            'data': knots[:, 1],
            'units': 'm',
            'quant': 'Z',
            'dim': 'distance',
            'ref': kk,
        },
        kcR: {
            'data': np.mean(knots[indices, 0], axis=1),
            'units': 'm',
            'quant': 'R',
            'dim': 'distance',
            'ref': kc,
        },
        kcZ: {
            'data': np.mean(knots[indices, 1], axis=1),
            'units': 'm',
            'quant': 'Z',
            'dim': 'distance',
            'ref': kc,
        },
        kii: {
            'data': indices,
            # 'units': '',
            'quant': 'indices',
            'dim': 'indices',
            'ref': (kc, ki),
        },
    }

    # dobj
    dmesh = {
        key: {
            'type': 'tri',
            'ntri': ntri,
            'cents': (kcR, kcZ),
            'knots': (kkR, kkZ),
            'ind': kii,
            # 'ref-k': (kk,),
            # 'ref-c': (kc,),
            'shape-c': (indices.shape[0],),
            'shape-k': (knots.shape[0],),
            'func_trifind': trifind,
            'crop': False,
        },
    }
    return dref, ddata, dmesh


# #############################################################################
# #############################################################################
#                           Mesh2DRect
# #############################################################################


def _mesh2DRect_X_check(
    x=None,
    res=None,
):
    """ Returns knots (x) and associated resolution

    res can be:
        - int: numbr of mesh elements desired between knots
        - float: desired average mesh element size
        - array of floats: (one for each x, desired approximate mesh size)

    """

    # ------------
    # Check inputs

    # x
    try:
        x = np.unique(np.ravel(x).astype(float))
    except Exception as err:
        msg = "x must be convertible to a sorted, flat array of floats!"
        raise Exception(msg)

    # res
    if res is None:
        res = 10

    lc = [
        isinstance(res, (int, np.int64, np.int32)) and len(x) == 2,
        isinstance(res, (float, np.floating)) and len(x) == 2,
        isinstance(res, (list, tuple, np.ndarray)) and len(x) == len(res),
    ]
    if not any(lc):
        msg = (
            "Arg res must be:\n"
            "\t- int: nb of mesh elements along x\n"
            "\t       requires len(x) = 2\n"
            "\t- float: approximate desired mesh element size along x\n"
            "\t       requires len(x) = 2\n"
            "\t- iterable: approximate desired mesh element sizes along x\n"
            "\t       requires len(x) = len(res)\n"
        )
        raise Exception(msg)

    if lc[0]:
        x_new = np.linspace(x[0], x[1], int(res)+1)
        res_new = res
        indsep = None

    elif lc[1]:
        nb = int(np.ceil((x[1]-x[0]) / res))
        x_new = np.linspace(x[0], x[1], nb+1)
        res_new = np.mean(np.diff(x))
        indsep = None

    else:

        # check conformity
        res = np.ravel(res).astype(float)
        delta = np.diff(x)
        res_sum = res[:-1] + res[1:]
        ind = res_sum > delta + 1.e-14
        if np.any(ind):
            msg = (
                "Desired resolution is not achievable for the following:\n"
                f"res_sum: {res_sum[ind]}\n"
                f"delta  : {delta[ind]}"
            )
            raise Exception(msg)

        # compute nn
        # nn = how many pairs can fit in the interval
        npairs = np.round(delta/res_sum).astype(int)
        res_sum_new = delta / npairs

        fract = res[:-1] / res_sum

        res_new = [None for ii in range(len(x)-1)]
        x_new = [None for ii in range(len(x)-1)]
        for ii in range(len(x)-1):
            res_new[ii] = (
                res_sum_new[ii]
                * np.linspace(fract[ii], 1.-fract[ii], 2*npairs[ii])
            )
            if ii == 0:
                res_add = np.concatenate(([0], np.cumsum(res_new[ii])))
            else:
                res_add = np.cumsum(res_new[ii])
            x_new[ii] = x[ii] + res_add

        indsep = np.cumsum(npairs[:-1]*2)
        res_new = np.concatenate(res_new)
        x_new = np.concatenate(x_new)

    return x_new, res_new, indsep


def _mesh1D_check(
    x=None,
    x_name=None,
    uniform=None,
):
    # R, Z check
    c0 = (
        hasattr(x, '__iter__')
        and np.asarray(x).ndim == 1
        and np.unique(x).size == np.array(x).size
        and np.allclose(np.unique(x), x)
    )
    if not c0:
        msg = f"Arg {x_name} must be convertible to a 1d increasing array"
        raise Exception(msg)

    x = np.unique(x)
    res = np.diff(x)
    ind = None

    # check uniformity
    if np.allclose(res, np.mean(res), atol=1e-12, rtol=0):
        res = res[0]

    elif uniform:
        msg = (
            "Non-uniform resolution for user-provided mesh {x_name}\n"
            f"\t- unique res: {np.unique(res)}\n"
            f"\t- diff res: {np.diff(np.unique(res))}\n"
            f"\t- res: {res}\n"
            )
        raise NotImplementedError(msg)
    return x, res, ind


def _mesh2DRect_check(
    domain=None,
    res=None,
    R=None,
    Z=None,
):

    # --------------
    # check inputs

    # (domain, res) vs (R, Z)
    lc = [
        domain is not None,
        R is not None and Z is not None,
    ]
    if all(lc) or not any(lc):
        msg = (
            "Please provide (domain, res) xor (R, Z), not both:\n"
            "Provided:\n"
            f"\t- domain, res: {domain}, {res}\n"
            f"\t- R, Z: {R}, {Z}\n"
        )
        raise Exception(msg)

    if lc[0]:
        # domain
        c0 = (
            isinstance(domain, list)
            and len(domain) == 2
            and all([
                hasattr(dd, '__iter__') and len(dd) >= 2 for dd in domain
            ])
        )
        if not c0:
            msg = (
                "Arg domain must be a list of 2 iterables of len() >= 2\n"
                f"Provided: {domain}"
            )
            raise Exception(msg)

        # res
        c0 = (
            res is None
            or np.isscalar(res)
            or isinstance(res, list) and len(res) == 2
        )
        if not c0:
            msg = (
                "Arg res must be a int, float or array or a list of 2 such\n"
                f"Provided: {res}"
            )
            raise Exception(msg)

        if np.isscalar(res) or res is None:
            res = [res, res]

        # -------------
        # check R and Z

        R, resR, indR = _mesh2DRect_X_check(domain[0], res=res[0])
        Z, resZ, indZ = _mesh2DRect_X_check(domain[1], res=res[1])

    elif lc[1]:

        # R
        R, resR, indR = _mesh1D_check(
            x=R,
            x_name='R',
            uniform=True,
        )

        # Z
        Z, resZ, indZ = _mesh1D_check(
            x=Z,
            x_name='Z',
            uniform=True,
        )

    return R, Z, resR, resZ, indR, indZ


def _mesh2DRect_to_dict(
    domain=None,
    res=None,
    R=None,
    Z=None,
    key=None,
):

    # --------------------
    # check / format input

    kRk, kRc, kkR, kcR = _mesh_names(key=key, x_name='R')
    kZk, kZc, kkZ, kcZ = _mesh_names(key=key, x_name='Z')

    R, Z, resR, resZ, indR, indZ = _mesh2DRect_check(
        domain=domain,
        res=res,
        R=R,
        Z=Z,
    )
    Rcent = 0.5*(R[1:] + R[:-1])
    Zcent = 0.5*(Z[1:] + Z[:-1])

    variable = not (np.isscalar(resR) and np.isscalar(resZ))

    # --------------------
    # prepare dict

    # dref
    dref = {
        kRk: {
            'size': R.size,
        },
        kZk: {
            'size': Z.size,
        },
        kRc: {
            'size': Rcent.size,
        },
        kZc: {
            'size': Zcent.size,
        },
    }

    # ddata
    ddata = {
        kkR: {
            'data': R,
            'units': 'm',
            # 'source': None,
            'dim': 'distance',
            'quant': 'R',
            'name': 'R',
            'ref': kRk,
        },
        kkZ: {
            'data': Z,
            'units': 'm',
            # 'source': None,
            'dim': 'distance',
            'quant': 'Z',
            'name': 'Z',
            'ref': kZk,
        },
        kcR: {
            'data': Rcent,
            'units': 'm',
            # 'source': None,
            'dim': 'distance',
            'quant': 'R',
            'name': 'R',
            'ref': kRc,
        },
        kcZ: {
            'data': Zcent,
            'units': 'm',
            # 'source': None,
            'dim': 'distance',
            'quant': 'Z',
            'name': 'Z',
            'ref': kZc,
        },
    }

    # dobj
    dmesh = {
        key: {
            'type': 'rect',
            'knots': (kkR, kkZ),
            'cents': (kcR, kcZ),
            # 'ref-k': (kRk, kZk),
            # 'ref-c': (kRc, kZc),
            'shape-c': (Rcent.size, Zcent.size),
            'shape-k': (R.size, Z.size),
            'variable': variable,
            'crop': False,
        },
    }
    return dref, ddata, dmesh


def _mesh2DRect_from_croppoly(crop_poly=None, domain=None):

    # ------------
    # check inputs

    c0 = hasattr(crop_poly, '__iter__') and len(crop_poly) == 2
    lc = [
        crop_poly is None,
        (
            c0
            and isinstance(crop_poly, tuple)
            and crop_poly[0].__class__.__name__ == 'Config'
            and (isinstance(crop_poly[1], str) or crop_poly[1] is None)
        )
        or crop_poly.__class__.__name__ == 'Config',
        c0
        and all([
            hasattr(cc, '__iter__') and len(cc) == len(crop_poly[0])
            for cc in crop_poly[1:]
        ])
        and np.asarray(crop_poly).ndim == 2
    ]

    if not any(lc):
        msg = (
            "Arg config must be a Config instance!"
        )
        raise Exception(msg)

    # -------------
    # Get polyand domain

    if lc[0]:
        # trivial case
        poly = None

    else:

        # -------------
        # Get poly from input

        if lc[1]:
            # (config, structure name)

            if crop_poly.__class__.__name__ == 'Config':
                config = crop_poly
                key_struct = None
            else:
                config, key_struct = crop_poly

            # key_struct if None
            if key_struct is None:
                lk, ls = zip(*[
                    (ss.Id.Name, ss.dgeom['Surf']) for ss in config.lStructIn
                ])
                key_struct = lk[np.argmin(ls)]

            # poly
            poly = config.dStruct['dObj']['Ves'][key_struct].Poly_closed

        else:

            # make sure poly is np.ndarraya and closed
            poly = np.asarray(crop_poly).astype(float)
            if not np.allclose(poly[:, 0], poly[:, -1]):
                poly = np.concatenate((poly, poly[:, 0:1]))

        # -------------
        # Get domain from poly

        if domain is None:
            domain = [
                [poly[0, :].min(), poly[0, :].max()],
                [poly[1, :].min(), poly[1, :].max()],
            ]

    return domain, poly


# #############################################################################
# #############################################################################
#                           Mesh2DRect - select
# #############################################################################


def _select_ind_check(
    ind=None,
    elements=None,
    returnas=None,
    crop=None,
    shape2d=None,
):

    # ----------------------
    # check basic conditions

    if shape2d:
        lc = [
            ind is None,
            isinstance(ind, tuple)
            and len(ind) == 2
            and (
                all([np.isscalar(ss) for ss in ind])
                or all([
                    hasattr(ss, '__iter__')
                    and len(ss) == len(ind[0])
                    for ss in ind
                ])
                or all([isinstance(ss, np.ndarray) for ss in ind])
            ),
            (
                np.isscalar(ind)
                or (
                    hasattr(ind, '__iter__')
                    and all([np.isscalar(ss) for ss in ind])
                )
                or isinstance(ind, np.ndarray)
            )
        ]

    else:
        lc = [
            ind is None,
            np.isscalar(ind)
            or (
                hasattr(ind, '__iter__')
                and all([np.isscalar(ss) for ss in ind])
            )
            or isinstance(ind, np.ndarray)
        ]

    # check lc
    if not any(lc):
        if shape2d:
            msg = (
                "Arg ind must be either:\n"
                "\t- None\n"
                "\t- int or array of int: int indices in mixed (R, Z) index\n"
                "\t- tuple of such: int indices in (R, Z) index respectively\n"
                f"Provided: {ind}"
            )
        else:
            msg = (
                "Arg ind must be either:\n"
                "\t- None\n"
                "\t- int or array of int: int indices\n"
                "\t- array of bool: bool indices\n"
                f"Provided: {ind}"
            )
        raise Exception(msg)

    # ----------------------
    # adapt to each case

    if lc[0]:
        pass

    elif lc[1] and shape2d:
        if any([not isinstance(ss, np.ndarray) for ss in ind]):
            ind = (
                np.atleast_1d(ind[0]).astype(int),
                np.atleast_1d(ind[1]).astype(int),
            )
        lc0 = [
            [
                isinstance(ss, np.ndarray),
                np.issubdtype(ss.dtype, np.integer),
                ss.shape == ind[0].shape,
            ]
                for ss in ind
        ]
        if not all([all(cc) for cc in lc0]):
            ltype = [type(ss) for ss in ind]
            ltypes = [
                ss.dtype if isinstance(ss, np.ndarray) else False
                for ss in ind
            ]
            lshapes = [
                ss.shape if isinstance(ss, np.ndarray) else len(ss)
                for ss in ind
            ]
            msg = (
                "Arg ind must be a tuple of 2 arrays of int of same shape\n"
                f"\t- lc0: {lc0}\n"
                f"\t- types: {ltype}\n"
                f"\t- type each: {ltypes}\n"
                f"\t- shape: {lshapes}\n"
                f"\t- ind: {ind}"
            )
            raise Exception(msg)

    elif lc[1] and not shape2d:
        if not isinstance(ind, np.ndarray):
            ind = np.atleast_1d(ind).astype(int)
        c0 = (
            np.issubdtype(ind.dtype, np.integer)
            or np.issubdtype(ind.dtype, np.bool_)
        )
        if not c0:
            msg = (
                "Arg ind must be an array of bool or int\n"
                f"Provided: {ind.dtype}"
            )
            raise Exception(msg)

    else:
        if not isinstance(ind, np.ndarray):
             ind = np.atleast_1d(ind).astype(int)
        c0 = (
            np.issubdtype(ind.dtype, np.integer)
            or np.issubdtype(ind.dtype, np.bool_)
        )
        if not c0:
            msg = (
                 "Arg ind must be an array of bool or int\n"
                 f"Provided: {ind.dtype}"
            )
            raise Exception(msg)

    # elements
    elements = ds._generic_check._check_var(
        elements, 'elements',
        types=str,
        default=_ELEMENTS,
        allowed=['knots', 'cents'],
    )

    # returnas
    if shape2d:
        retdef = tuple
        retok = [tuple, np.ndarray, 'tuple-flat', 'array-flat', bool]
    else:
        retdef = bool
        retok = [int, bool]

    returnas = ds._generic_check._check_var(
        returnas, 'returnas',
        types=None,
        default=retdef,
        allowed=retok,
    )

    # crop
    crop = ds._generic_check._check_var(
        crop, 'crop',
        types=bool,
        default=True,
    )

    return ind, elements, returnas, crop


def _select_check(
    elements=None,
    returnas=None,
    return_ind_as=None,
    return_neighbours=None,
):

    # elements
    elements = ds._generic_check._check_var(
        elements, 'elements',
        types=str,
        default=_ELEMENTS,
        allowed=['knots', 'cents'],
    )

    # returnas
    returnas = ds._generic_check._check_var(
        returnas, 'returnas',
        types=None,
        default='ind',
        allowed=['ind', 'data'],
    )

    # return_ind_as
    return_ind_as = ds._generic_check._check_var(
        return_ind_as, 'return_ind_as',
        types=None,
        default=int,
        allowed=[int, bool],
    )

    # return_neighbours
    return_neighbours = ds._generic_check._check_var(
        return_neighbours, 'return_neighbours',
        types=bool,
        default=True,
    )

    return elements, returnas, return_ind_as, return_neighbours
