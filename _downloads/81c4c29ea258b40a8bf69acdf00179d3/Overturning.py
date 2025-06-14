#!/usr/bin/env python

"""
veros run --force-overwrite Overturning.py -s identifier OverturningBeta1e5Coarse -s nz 18 -s dt_mom 3000 -s kappaM_0 1e-5 -s kappaH_0 1e-5 -s runlen 124_416_000_000

veros run --force-overwrite Overturning.py -s identifier OverturningBeta4e5Coarse -s nz 18 -s dt_mom 3000 -s kappaM_0 4e-5 -s kappaH_0 4e-5 -s runlen 124_416_000_000

veros run --force-overwrite Overturning.py -s identifier OverturningBeta1e4Coarse -s nz 18 -s dt_mom 3000 -s kappaM_0 1e-4 -s kappaH_0 1e-4 -s runlen 124_416_000_000

veros run --force-overwrite Overturning.py -s identifier OverturningBeta4e4Coarse -s nz 18 -s dt_mom 3000 -s kappaM_0 4e-4 -s kappaH_0 4e-4 -s runlen 124_416_000_000

veros run --force-overwrite Overturning.py -s identifier OverturningBeta4e4Coarse -s nz 18 -s dt_mom 3000 -s kappaM_0 8e-5 -s kappaH_0 8e-5 -s runlen 124_416_000_000

veros run --force-overwrite Overturning.py -s identifier OverturningBeta4e6Coarse -s nz 18 -s dt_mom 3000 -s kappaM_0 0.4e-5 -s kappaH_0 0.4e-5 -s runlen 124_416_000_000


"""

__VEROS_VERSION__ = '1.5.0'

if __name__ == "__main__":
    raise RuntimeError(
        "Veros setups cannot be executed directly. "
        f"Try `veros run {__file__}` instead."
    )

# -- end of auto-generated header, original file below --


from veros import VerosSetup, veros_routine, veros_kernel, KernelOutput
from veros.variables import allocate, Variable
from veros.distributed import global_min, global_max
from veros.core.operators import numpy as npx, update, at

import matplotlib.pyplot as plt

maxx = 0
maxy = 0
maxdepth = 4000

class BasinSetup(VerosSetup):
    """A model using cartesian coordinates in basin no beta effect

    Wind forcing over a channel; no buoyancy

    """


    @veros_routine
    def set_parameter(self, state):
        settings = state.settings
        settings.identifier = "OverturningBeta"

        settings.nx, settings.ny, settings.nz = 12, 18, 30

        settings.dt_mom = 4800 / 2
        settings.dt_tracer = 86400
        settings.runlen = 3600 * 24 * 30 * 12 * 1000

        settings.x_origin = 0.0
        settings.y_origin = 0.0

        settings.coord_degree = True
        settings.enable_cyclic_x = False

        settings.enable_neutral_diffusion = True
        settings.K_iso_0 = 1000.0
        settings.K_iso_steep = 500.0
        settings.iso_dslope = 0.005
        settings.iso_slopec = 0.01
        settings.enable_skew_diffusion = True

        settings.enable_hor_friction = True
        # settings.enable_hor_diffusion = True
        dx = settings.degtom * 4
        settings.A_h = (dx) ** 3 * 2e-11
        settings.K_h = settings.A_h
        settings.enable_hor_friction_cos_scaling = True
        settings.hor_friction_cosPower = 1

        settings.A_hbi = (3.5e5) ** 3 * 2e-11 * (3.5e5)**2 / 8
        settings.K_hbi = (3.5e5) ** 3 * 2e-11 * (3.5e5)**2 / 8

        # check dt:
        dt = dx**4 / 32 / settings.A_hbi
        print('dt', dt, 'dt_mom', settings.dt_mom)
        # assert dt > 2 * settings.dt_mom

        dt = dx**2 / 4 / settings.K_h
        print('dt', dt, 'dt_tracer', settings.dt_tracer)
        # assert dt > 2 * settings.dt_tracer

        settings.enable_superbee_advection = False

        #settings.enable_quadratic_bottom_friction = True
        #settings.r_quad_bot = 1e-1


        settings.enable_implicit_vert_friction = True

        if False:
            settings.enable_tke = True
            settings.c_k = 0.1
            settings.c_eps = 0.7
            settings.alpha_tke = 30.0
            settings.mxl_min = 1e-8
            settings.tke_mxl_choice = 2
            settings.kappaM_min = 1e-5
            settings.kappaH_min = 1e-5
            settings.enable_kappaH_profile = True

            settings.K_gm_0 = 1000.0
            settings.enable_eke = True
            settings.eke_k_max = 1e4
            settings.eke_c_k = 0.4
            settings.eke_c_eps = 0.5
            settings.eke_cross = 2.0
            settings.eke_crhin = 1.0
            settings.eke_lmin = 100.0
            settings.enable_eke_superbee_advection = True
            settings.enable_eke_isopycnal_diffusion = True

        settings.kappaM_0 = 1e-4
        settings.kappaH_0 = 1e-4

        settings.enable_streamfunction = False

        settings.enable_idemix = False
        settings.enable_noslip_lateral = False

        settings.eq_of_state_type = 1

        settings.restart_frequency = 3600 * 24 * 30 * 12 * 10

    @veros_routine
    def set_grid(self, state):
        global maxx
        global maxy
        global maxdepth

        vs = state.variables
        settings = state.settings

        # ddz = 1000 / settings.nz

        ddz = npx.exp(-npx.arange(settings.nz) / 14)
        ddz = ddz / npx.sum(ddz) * maxdepth

        ddx = 4  # degrees
        maxx = settings.nx * ddx
        maxy = settings.ny * ddx

        vs.dxt = update(vs.dxt, at[...], ddx)
        vs.dyt = update(vs.dyt, at[...], ddx)
        vs.dzt = update(vs.dzt, at[...], ddz)

    @veros_routine
    def set_coriolis(self, state):
        vs = state.variables
        settings = state.settings
        vs.coriolis_t = update(
            vs.coriolis_t, at[:, :], 2 * settings.omega * npx.sin(vs.yt[None, :] / 180.0 * settings.pi)
        )

    @veros_routine
    def set_topography(self, state):
        vs = state.variables
        settings = state.settings
        depths = -maxdepth * npx.ones((settings.nx, settings.ny))
        if False:
            global maxx
            global maxy
            print('MAX', maxx)
            depths = (npx.interp(vs.xt[2:-2], [0, 150e-10, maxx-150e-10, maxx], [0, 1, 1, 0])[:, npx.newaxis] *
                    npx.interp(vs.yt[2:-2], [0, 150e-10, maxy-150e-10, maxy], [0, 1, 1, 0])[npx.newaxis, :])
            depths = - depths * 1000

        depth_levels = 1 + npx.argmin(npx.abs(depths[:, :, npx.newaxis] - vs.zt[npx.newaxis, npx.newaxis, :]), axis=2)
        vs.kbot = update(vs.kbot, at[2:-2, 2:-2], npx.where(depth_levels > 0.0, depth_levels, 0))
        vs.kbot = npx.where(vs.kbot < settings.nz, vs.kbot, 0)

        # depth of deepest cell.  0 is land,  1 is deepest
        # nz is shallowest..
        if False:
            dd = npx.array([settings.nz+1, 1, 1, settings.nz+1])
            yy = npx.array([0, 500, 20000-500, 20000])
            k = npx.interp(vs.yt, yy, dd)
            k = npx.where(k>settings.nz, 0, k)  # land
            k = npx.floor(k)
        # vs.kbot = update(vs.kbot, at[...], k)

    @veros_routine
    def set_initial_conditions(self, state):

        vs = state.variables
        settings = state.settings

        temp = npx.ones(settings.nz) * 4   # 4 degrees
        temp = npx.linspace(4, 4.04, settings.nz)

        vs.temp = update(vs.temp, at[...],
                         temp[npx.newaxis, npx.newaxis, :, npx.newaxis])

        vs.salt = update(vs.salt, at[...], 35)


    @veros_routine
    def set_forcing(self, state):
        vs = state.variables
        vs.update(set_forcing_kernel(state))


    @veros_routine
    def set_diagnostics(self, state):
        settings = state.settings
        diagnostics = state.diagnostics

        diagnostics["snapshot"].output_frequency = 24 * 3600 * 30 * 12  # yearly
        diagnostics["overturning"].output_frequency = 24 * 3600 * 30 * 12 * 20  # 20 years
        diagnostics["overturning"].sampling_frequency = settings.dt_tracer * 10

    @veros_routine
    def after_timestep(self, state):
        pass

@veros_kernel
def set_forcing_kernel(state):
    vs = state.variables

    global maxy
    sst = 16 - 12 * npx.cos((maxy - vs.yt) * npx.pi / maxy)
    sst = npx.clip(sst, 4, 30)
    # Model wants heat flux is in K m/s.  Measured heat flux is order 100 W /m^2.
    # If dT = 10 C, Cp = 4000 J / C / kg, then wpiston = 2.5e-6 m/s

    # Bryan 87 uses 20 / 25 days = 9.3e-6 m/s.  So lets use 10e-6

    vs.forc_temp_surface = (sst - vs.temp[:, :, -1, vs.tau]) * vs.maskT[:, :, -1] * 100e-6

    return KernelOutput(
        forc_temp_surface=vs.forc_temp_surface,
    )