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
#                   names of knots and cents
# #############################################################################


def names_knots_cents(key=None, knots_name=None):
    kkr, kcr = f'{key}-{knots_name}-nk', f'{key}-{knots_name}-nc'
    kk, kc = f'{key}-k-{knots_name}', f'{key}-c-{knots_name}'
    return kkr, kcr, kk, kc


# #############################################################################
# #############################################################################
#               mesh vs bsplines
# #############################################################################


def _get_key_mesh_vs_bplines(
    coll=None,
    key=None,
    which=None,
):
    
    if which in [None, coll._which_mesh]:
        lk1 = list(coll.dobj.get(coll._which_mesh, {}).keys())
    else:
        lk1 = []
    
    if which in [None, coll._which_bsplines]:
        lk2 = list(coll.dobj.get(coll._which_bsplines, {}).keys())
    else:
        lk2 = []
        
    # key
    key = ds._generic_check._check_var(
        key, 'key',
        allowed=lk1 + lk2,
        types=str,
    )
    
    # which
    if key in lk1:
        cat = coll._which_mesh
    else:
        cat = coll._which_bsplines
    assert which in [cat, None], (cat, which)

    # keys
    if cat == coll._which_bsplines:
        keym = coll.dobj[coll._which_bsplines][key][coll._which_mesh]
        keybs = key
    else:
        keym = key
        keybs = None
        
    return keym, keybs, cat
    

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

    return elements, returnas, return_ind_as, return_neighbours,


# #############################################################################
# #############################################################################
#                           Mesh2DRect - bsplines
# #############################################################################


def _mesh_bsplines(key=None, lkeys=None, deg=None):

    # key
    key = ds._generic_check._check_var(
        key, 'key',
        types=str,
        allowed=lkeys,
    )

    # deg
    deg = ds._generic_check._check_var(
        deg, 'deg',
        types=int,
        default=2,
        allowed=[0, 1, 2, 3],
    )

    # keybs
    keybs = f'{key}-bs{deg}'

    return key, keybs, deg
