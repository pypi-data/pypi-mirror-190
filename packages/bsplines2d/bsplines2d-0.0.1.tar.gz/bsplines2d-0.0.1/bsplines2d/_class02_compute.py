# -*- coding: utf-8 -*-


# Built-in


# Common
import numpy as np
import datastock as ds


# tofu
from . import _utils_bsplines
# from . import _class02_checks as _checks
from . import _class02_bsplines_rect
from . import _class02_bsplines_tri
from . import _class02_bsplines_polar
from . import _class02_bsplines_1d



# ##################################################################
# ##################################################################
#                           Mesh1D - bsplines
# ##################################################################


def _mesh1d_bsplines(
    coll=None,
    keym=None,
    keybs=None,
    deg=None,
):

    kknots = coll.dobj[coll._which_mesh][keym]['knots'][0]
    knots = coll.ddata[kknots]['data']

    kbsn = f'{keybs}_nbs'
    kbsap = f'{keybs}_ap'

    clas = _class02_bsplines_1d.get_bs_class(
        deg=deg,
        knots=knots,
        coll=coll,
    )

    # ------------
    # refs

    ref = (kbsn,)
    apex = (kbsap,)

    # ----------------
    # format into dict

    # dref
    dref = {
        # bs index
        kbsn: {'size': clas.nbs},
    }

    # ddata
    ddata = {
        kbsap: {
            'data': clas.apex_per_bs,
            'units': coll.ddata[kknots]['units'],
            'dim': coll.ddata[kknots]['dim'],
            'quant': coll.ddata[kknots]['quant'],
            'name': coll.ddata[kknots]['name'],
            'ref': (kbsn,),
        },
    }

    # dobj
    wm = coll._which_mesh
    wbs = coll._which_bsplines
    dobj = {
        wbs: {
            keybs: {
                'deg': deg,
                wm: keym,
                'ref': ref,
                'ref-bs': (kbsn,),
                'apex': apex,
                'shape': clas.shapebs,
                'class': clas,
                'crop': None,
            }
        },
    }

    return dref, ddata, dobj


# ################################################################
# ################################################################
#                           Mesh2DRect - bsplines
# ################################################################


def _mesh2DRect_bsplines(coll=None, keym=None, keybs=None, deg=None):

    # --------------
    # create bsplines

    k0, k1 = coll.dobj[coll._which_mesh][keym]['knots']
    knots0 = coll.ddata[k0]['data']
    knots1 = coll.ddata[k1]['data']

    keybsr = f'{keybs}_nbs'
    kRbsapn = f'{keybs}_nR'
    kZbsapn = f'{keybs}_nZ'
    kRbsap = f'{keybs}_apR'
    kZbsap = f'{keybs}_apZ'

    (
        shapebs, Rbs_apex, Zbs_apex,
        knots_per_bs_R, knots_per_bs_Z,
    ) = _class02_bsplines_rect.get_bs2d_x01(
        deg=deg, knots0=knots0, knots1=knots1,
    )
    nbs = int(np.prod(shapebs))

    clas = _class02_bsplines_rect.get_bs_class(
        deg=deg,
        knots0=knots0,
        knots1=knots1,
        shapebs=shapebs,
        # knots_per_bs_R=knots_per_bs_R,
        # knots_per_bs_Z=knots_per_bs_Z,
    )

    # ----------------
    # format into dict

    dref = {
        kRbsapn: {
            'size': Rbs_apex.size,
        },
        kZbsapn: {
            'size': Zbs_apex.size,
        },
        keybsr: {
            'size': nbs,
        },
    }

    ddata = {
        kRbsap: {
            'data': Rbs_apex,
            'units': coll.ddata[k0]['units'],
            'dim': coll.ddata[k0]['dim'],
            'quant': coll.ddata[k0]['quant'],
            'name': coll.ddata[k0]['name'],
            'ref': kRbsapn,
        },
        kZbsap: {
            'data': Zbs_apex,
            'units': coll.ddata[k1]['units'],
            'dim': coll.ddata[k1]['dim'],
            'quant': coll.ddata[k1]['quant'],
            'name': coll.ddata[k1]['name'],
            'ref': kZbsapn,
        },
    }

    dobj = {
        'bsplines': {
            keybs: {
                'deg': deg,
                'mesh': keym,
                'ref': (kRbsapn, kZbsapn),
                'ref-bs': (keybsr,),
                'apex': (kRbsap, kZbsap),
                'shape': shapebs,
                'crop': False,
                'class': clas,
            }
        },
    }

    return dref, ddata, dobj


def _mesh2DRect_bsplines_knotscents(
    returnas=None,
    return_knots=None,
    return_cents=None,
    ind=None,
    deg=None,
    Rknots=None,
    Zknots=None,
    Rcents=None,
    Zcents=None,
):

    # -------------
    # check inputs

    return_knots = ds._generic_check._check_var(
        return_knots, 'return_knots',
        types=bool,
        default=True,
    )
    return_cents = ds._generic_check._check_var(
        return_cents, 'return_cents',
        types=bool,
        default=True,
    )
    if return_knots is False and return_cents is False:
        return

    # -------------
    # compute

    if return_knots is True:

        knots_per_bs_R = _utils_bsplines._get_knots_per_bs(
            Rknots, deg=deg, returnas=returnas,
        )
        knots_per_bs_Z = _utils_bsplines._get_knots_per_bs(
            Zknots, deg=deg, returnas=returnas,
        )
        if ind is not None:
            knots_per_bs_R = knots_per_bs_R[:, ind[0]]
            knots_per_bs_Z = knots_per_bs_Z[:, ind[1]]

        nknots = knots_per_bs_R.shape[0]
        knots_per_bs_R = np.tile(knots_per_bs_R, (nknots, 1))
        knots_per_bs_Z = np.repeat(knots_per_bs_Z, nknots, axis=0)

    if return_cents is True:

        cents_per_bs_R = _utils_bsplines._get_cents_per_bs(
            Rcents, deg=deg, returnas=returnas,
        )
        cents_per_bs_Z = _utils_bsplines._get_cents_per_bs(
            Zcents, deg=deg, returnas=returnas,
        )
        if ind is not None:
            cents_per_bs_R = cents_per_bs_R[:, ind[0]]
            cents_per_bs_Z = cents_per_bs_Z[:, ind[1]]

        ncents = cents_per_bs_R.shape[0]
        cents_per_bs_R = np.tile(cents_per_bs_R, (ncents, 1))
        cents_per_bs_Z = np.repeat(cents_per_bs_Z, ncents, axis=0)

    # -------------
    # return

    if return_knots is True and return_cents is True:
        out = (
            (knots_per_bs_R, knots_per_bs_Z), (cents_per_bs_R, cents_per_bs_Z)
        )
    elif return_knots is True:
        out = (knots_per_bs_R, knots_per_bs_Z)
    else:
        out = (cents_per_bs_R, cents_per_bs_Z)
    return out


# ##################################################################
# ##################################################################
#                           Mesh2 - Tri - bsplines
# ##################################################################


def _mesh2DTri_bsplines(coll=None, keym=None, keybs=None, deg=None):

    # --------------
    # create bsplines

    kknots = coll.dobj[coll._which_mesh][keym]['knots']
    clas = _class02_bsplines_tri.get_bs_class(
        deg=deg,
        knots0=coll.ddata[kknots[0]]['data'],
        knots1=coll.ddata[kknots[1]]['data'],
        indices=coll.ddata[coll.dobj[coll._which_mesh][keym]['ind']]['data'],
    )
    keybsr = f'{keybs}-nbs'
    kbscr = f'{keybs}-apR'
    kbscz = f'{keybs}-apZ'

    bs_cents = clas._get_bs_cents()

    # ----------------
    # format into dict

    dref = {
        # bs index
        keybsr: {
            'size': clas.nbs,
        },
    }

    ddata = {
        kbscr: {
            'data': bs_cents[0, :],
            'units': coll.ddata[kknots[0]]['units'],
            'dim': coll.ddata[kknots[0]]['dim'],
            'quant': coll.ddata[kknots[0]]['quant'],
            'name': coll.ddata[kknots[0]]['name'],
            'ref': (keybsr,),
        },
        kbscz: {
            'data': bs_cents[1, :],
            'units': coll.ddata[kknots[1]]['units'],
            'dim': coll.ddata[kknots[1]]['dim'],
            'quant': coll.ddata[kknots[1]]['quant'],
            'name': coll.ddata[kknots[1]]['name'],
            'ref': (keybsr,),
        },
    }

    dobj = {
        'bsplines': {
            keybs: {
                'deg': deg,
                'mesh': keym,
                'ref': (keybsr,),
                'ref-bs': (keybsr,),
                'apex': (kbscr, kbscz),
                'shape': (clas.nbs,),
                'crop': False,
                'class': clas,
            }
        },
    }

    return dref, ddata, dobj


# ##################################################################
# ##################################################################
#                           Mesh2D - polar - bsplines
# ##################################################################


# def _mesh2Dpolar_bsplines(
    # coll=None,
    # keym=None,
    # keybs=None,
    # angle=None,
    # deg=None,
# ):

    # # ---------------
    # # create bsplines

    # kknots = coll.dobj[coll._which_mesh][keym]['knots']
    # knotsr = coll.ddata[kknots[0]]['data']
    # if len(kknots) == 2:
        # angle = coll.ddata[kknots[1]]['data']

    # clas = _class02_bsplines_polar.get_bs2d_func(
        # deg=deg,
        # knotsr=knotsr,
        # angle=angle,
        # coll=coll,
    # )

    # keybsnr = f'{keybs}-nr'
    # keybsn = f'{keybs}-nbs'
    # keybsapr = f'{keybs}-apr'

    # # ------------
    # # refs

    # if clas.knotsa is None:
        # ref = (keybsnr,)
        # apex = (keybsapr,)
    # elif len(clas.shapebs) == 2:
        # keybsna = f'{keybs}-na'
        # keybsapa = f'{keybs}-apa'
        # ref = (keybsnr, keybsna)
        # apex = (keybsapr, keybsapa)
    # else:
        # ref = (keybsn,)
        # apex = (keybsapr,)

        # # check angle vs angle2d
        # mesh = coll._which_mesh
        # angle2d = coll.dobj[mesh][keym]['angle2d']
        # if angle2d is None:
            # msg = (
                # "Poloidal bsplines require mesh with angle2d!\n"
                # f"\t- self.dobj['{mesh}']['{keym}']['angle2d'] = {angle2d}"
            # )
            # raise Exception(msg)

    # # bs_cents = clas._get_bs_cents()

    # # ----------------
    # # format into dict

    # # dref
    # dref = {
        # # bs index
        # keybsnr: {'size': clas.nbs_r},
        # keybsn: {'size': clas.nbs},
    # }
    # if len(clas.shapebs) == 2:
        # dref[keybsna] = {'size': clas.nbs_a_per_r[0]}

    # # ddata
    # ddata = {
        # keybsapr: {
            # 'data': clas.apex_per_bs_r,
            # 'units': '',
            # 'dim': '',
            # 'quant': '',
            # 'name': '',
            # 'ref': (keybsnr,),
        # },
    # }
    # if len(clas.shapebs) == 2:
        # ddata[keybsapa] = {
            # 'data': clas.apex_per_bs_a[0],
            # 'units': 'rad',
            # 'dim': 'angle',
            # 'quant': '',
            # 'name': '',
            # 'ref': (keybsna,),
        # }

    # # dobj
    # dobj = {
        # 'bsplines': {
            # keybs: {
                # 'deg': deg,
                # 'mesh': keym,
                # 'ref': ref,
                # 'ref-bs': (keybsn,),
                # 'apex': apex,
                # 'shape': clas.shapebs,
                # 'class': clas,
                # 'crop': coll.dobj[coll._which_mesh][keym]['crop'],
            # }
        # },
    # }

    # return dref, ddata, dobj


# def _mesh2DPolar_bsplines_knotscents(
    # returnas=None,
    # return_knots=None,
    # return_cents=None,
    # ind=None,
    # deg=None,
    # # resources
    # clas=None,
    # rknots=None,
    # aknots=None,
    # rcents=None,
    # acents=None,
# ):

    # # -------------
    # # check inputs

    # return_knots = ds._generic_check._check_var(
        # return_knots, 'return_knots',
        # types=bool,
        # default=True,
    # )
    # return_cents = ds._generic_check._check_var(
        # return_cents, 'return_cents',
        # types=bool,
        # default=True,
    # )
    # if return_knots is False and return_cents is False:
        # return

    # # -------------
    # # compute

    # if return_knots is True:

        # knots_per_bs_r = _utils_bsplines._get_knots_per_bs(
            # rknots, deg=deg, returnas=returnas,
        # )
        # knots_per_bs_Z = _utils_bsplines._get_knots_per_bs(
            # Zknots, deg=deg, returnas=returnas,
        # )
        # if ind is not None:
            # knots_per_bs_R = knots_per_bs_R[:, ind[0]]
            # knots_per_bs_Z = knots_per_bs_Z[:, ind[1]]

        # nknots = knots_per_bs_R.shape[0]
        # knots_per_bs_R = np.tile(knots_per_bs_R, (nknots, 1))
        # knots_per_bs_Z = np.repeat(knots_per_bs_Z, nknots, axis=0)

    # if return_cents is True:

        # cents_per_bs_R = _utils_bsplines._get_cents_per_bs(
            # Rcents, deg=deg, returnas=returnas,
        # )
        # cents_per_bs_Z = _utils_bsplines._get_cents_per_bs(
            # Zcents, deg=deg, returnas=returnas,
        # )
        # if ind is not None:
            # cents_per_bs_R = cents_per_bs_R[:, ind[0]]
            # cents_per_bs_Z = cents_per_bs_Z[:, ind[1]]

        # ncents = cents_per_bs_R.shape[0]
        # cents_per_bs_R = np.tile(cents_per_bs_R, (ncents, 1))
        # cents_per_bs_Z = np.repeat(cents_per_bs_Z, ncents, axis=0)

    # # -------------
    # # return

    # if return_knots is True and return_cents is True:
        # out = (
            # (knots_per_bs_R, knots_per_bs_Z), (cents_per_bs_R, cents_per_bs_Z)
        # )
    # elif return_knots is True:
        # out = (knots_per_bs_R, knots_per_bs_Z)
    # else:
        # out = (cents_per_bs_R, cents_per_bs_Z)
    # return out


# #############################################################################
# #############################################################################
#                           Mesh2DRect - interp utility
# #############################################################################


# def _get_keyingroup_ddata(
    # dd=None, dd_name='data',
    # key=None, monot=None,
    # msgstr=None, raise_=False,
# ):
    # """ Return the unique data key matching key

    # Here, key can be interpreted as name / source / units / quant...
    # All are tested using select() and a unique match is returned
    # If not unique match an error message is either returned or raised

    # """

    # # ------------------------
    # # Trivial case: key is actually a ddata key

    # if key in dd.keys():
        # return key, None

    # # ------------------------
    # # Non-trivial: check for a unique match on other params

    # dind = _select(
        # dd=dd, dd_name=dd_name,
        # dim=key, quant=key, name=key, units=key, source=key,
        # monot=monot,
        # log='raw',
        # returnas=bool,
    # )
    # ind = np.array([ind for kk, ind in dind.items()])

    # # Any perfect match ?
    # nind = np.sum(ind, axis=1)
    # sol = (nind == 1).nonzero()[0]
    # key_out, msg = None, None
    # if sol.size > 0:
        # if np.unique(sol).size == 1:
            # indkey = ind[sol[0], :].nonzero()[0]
            # key_out = list(dd.keys())[indkey]
        # else:
            # lstr = "[dim, quant, name, units, source]"
            # msg = "Several possible matches in {} for {}".format(lstr, key)
    # else:
        # lstr = "[dim, quant, name, units, source]"
        # msg = "No match in {} for {}".format(lstr, key)

    # # Complement error msg and optionally raise
    # if msg is not None:
        # lk = ['dim', 'quant', 'name', 'units', 'source']
        # dk = {
            # kk: (
                # dind[kk].sum(),
                # sorted(set([vv[kk] for vv in dd.values()]))
            # ) for kk in lk
        # }
        # msg += (
            # "\n\nRequested {} could not be identified!\n".format(msgstr)
            # + "Please provide a valid (unique) key/name/dim/quant/units:\n\n"
            # + '\n'.join([
                # '\t- {} ({} matches): {}'.format(kk, dk[kk][0], dk[kk][1])
                # for kk in lk
            # ])
            # + "\nProvided:\n\t'{}'".format(key)
        # )
        # if raise_:
            # raise Exception(msg)
    # return key_out, msg

"""
def _get_possible_ref12d(
    dd=None,
    key=None, ref1d=None, ref2d=None,
    group1d='radius',
    group2d='mesh2d',
):

    # Get relevant lists
    kq, msg = _get_keyingroup_ddata(
        dd=dd,
        key=key, group=group2d, msgstr='quant', raise_=False,
    )

    if kq is not None:
        # The desired quantity is already 2d
        k1d, k2d = None, None

    else:
        # Check if the desired quantity is 1d
        kq, msg = _get_keyingroup_ddata(
            dd=dd,
            key=key, group=group1d,
            msgstr='quant', raise_=True,
        )

        # Get dict of possible {ref1d: lref2d}
        ref = [rr for rr in dd[kq]['ref'] if dd[rr]['group'] == (group1d,)][0]
        lref1d = [
            k0 for k0, v0 in dd.items()
            if ref in v0['ref'] and v0['monot'][v0['ref'].index(ref)] is True
        ]

        # Get matching ref2d with same quant and good group
        lquant = list(set([dd[kk]['quant'] for kk in lref1d]))
        dref2d = {
            k0: [
                kk for kk in _select(
                    dd=dd, quant=dd[k0]['quant'],
                    log='all', returnas=str,
                )
                if group2d in dd[kk]['group']
                and not isinstance(dd[kk]['data'], dict)
            ]
            for k0 in lref1d
        }
        dref2d = {k0: v0 for k0, v0 in dref2d.items() if len(v0) > 0}

        if len(dref2d) == 0:
            msg = (
                "No match for (ref1d, ref2d) for ddata['{}']".format(kq)
            )
            raise Exception(msg)

        # check ref1d
        if ref1d is None:
            if ref2d is not None:
                lk = [k0 for k0, v0 in dref2d.items() if ref2d in v0]
                if len(lk) == 0:
                    msg = (
                        "\nNon-valid interpolation intermediate\n"
                        + "\t- provided:\n"
                        + "\t\t- ref1d = {}, ref2d = {}\n".format(ref1d, ref2d)
                        + "\t- valid:\n{}".format(
                            '\n'.join([
                                '\t\t- ref1d = {}  =>  ref2d in {}'.format(
                                    k0, v0
                                )
                                for k0, v0 in dref2d.items()
                            ])
                        )
                    )
                    raise Exception(msg)
                if kq in lk:
                    ref1d = kq
                else:
                    ref1d = lk[0]
            else:
                if kq in dref2d.keys():
                    ref1d = kq
                else:
                    ref1d = list(dref2d.keys())[0]
        else:
            ref1d, msg = _get_keyingroup_ddata(
                dd=dd,
                key=ref1d, group=group1d,
                msgstr='ref1d', raise_=False,
            )
        if ref1d not in dref2d.keys():
            msg = (
                "\nNon-valid interpolation intermediate\n"
                + "\t- provided:\n"
                + "\t\t- ref1d = {}, ref2d = {}\n".format(ref1d, ref2d)
                + "\t- valid:\n{}".format(
                    '\n'.join([
                        '\t\t- ref1d = {}  =>  ref2d in {}'.format(
                            k0, v0
                        )
                        for k0, v0 in dref2d.items()
                    ])
                )
            )
            raise Exception(msg)

        # check ref2d
        if ref2d is None:
            ref2d = dref2d[ref1d][0]
        else:
            ref2d, msg = _get_keyingroup_ddata(
                dd=dd,
                key=ref2d, group=group2d,
                msgstr='ref2d', raise_=False,
            )
        if ref2d not in dref2d[ref1d]:
            msg = (
                "\nNon-valid interpolation intermediate\n"
                + "\t- provided:\n"
                + "\t\t- ref1d = {}, ref2d = {}\n".format(ref1d, ref2d)
                + "\t- valid:\n{}".format(
                    '\n'.join([
                        '\t\t- ref1d = {}  =>  ref2d in {}'.format(
                            k0, v0
                        )
                        for k0, v0 in dref2d.items()
                    ])
                )
            )
            raise Exception(msg)

    return (
        kq, ref1d, ref2d,
        coll=None,
        key=None,
        R=None,
        Z=None,
        indbs=None,
        indt=None,
        grid=None,
        details=None,
        reshape=None,
        res=None,
        crop=None,
        nan0=None,
        imshow=None,
        return_params=None,
    )
):

    # ---------------
    # check inputs

    # TBD
    pass

    # ---------------
    # post-treatment

    if nan0 is True:
        val[val == 0] = np.nan

    # ------
    # return

    if return_params is True:
        return val, dparams
    else:
        return val
"""
