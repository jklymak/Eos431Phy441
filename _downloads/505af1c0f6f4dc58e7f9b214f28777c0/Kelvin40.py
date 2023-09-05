#!/usr/bin/env python

"""
"""

__VEROS_VERSION__ = '1.4.2+365.gfd1e6a5'

if __name__ == "__main__":
    raise RuntimeError(
        "Veros setups cannot be executed directly. "
        f"Try `veros run {__file__}` instead."
    )

# -- end of auto-generated header, original file below --


from veros import VerosSetup, veros_routine
from veros.variables import allocate, Variable
from veros.distributed import global_min, global_max
from veros.core.operators import numpy as npx, update, at

import matplotlib.pyplot as plt

class BasinSetup(VerosSetup):
    """A model using cartesian coordinates in basin no beta effect

    Wind forcing over a channel; no buoyancy

    """

    @veros_routine
    def set_parameter(self, state):
        settings = state.settings
        settings.identifier = "Kelvin40"

        settings.nx, settings.ny, settings.nz = 160, 160, 10

        settings.dt_mom = 120 * 2
        settings.dt_tracer = settings.dt_mom
        settings.runlen = 3600 * 24 * 10

        settings.x_origin = 0.0
        settings.y_origin = 0.0

        settings.coord_degree = False
        settings.enable_cyclic_x = False

        settings.enable_neutral_diffusion = False

        settings.enable_hor_friction = True
        settings.enable_hor_diffusion = True
        settings.A_h = 4
        settings.K_h = settings.A_h
        settings.enable_hor_friction_cos_scaling = False
        settings.hor_friction_cosPower = 1

        settings.enable_quadratic_bottom_friction = True
        settings.r_quad_bot = 1e-1

        settings.enable_implicit_vert_friction = True
        settings.enable_explicit_vert_friction = False

        settings.kappaM_0 = 1e-4
        settings.kappaH_0 = 1e-4

        settings.enable_streamfunction = False

        settings.enable_idemix = False
        settings.enable_noslip_lateral = False

        settings.eq_of_state_type = 1

    @veros_routine
    def set_grid(self, state):
        vs = state.variables
        settings = state.settings

        ddz = 200 / settings.nz
        vs.dxt = update(vs.dxt, at[...], 2000)
        vs.dyt = update(vs.dyt, at[...], 2000)
        vs.dzt = update(vs.dzt, at[...], ddz)

    @veros_routine
    def set_coriolis(self, state):
        vs = state.variables
        # settings = state.settings
        cor = 1e-4 + vs.yt * 1e-10
        vs.coriolis_t = update(
            vs.coriolis_t, at[...], cor
        )
        print(vs.coriolis_t)

    @veros_routine
    def set_topography(self, state):
        vs = state.variables
        settings = state.settings
        # depth of deepest cell.  0 is land,  1 is deepest
        # nz is shallowest..
        if False:
            dd = npx.array([settings.nz+1, 1, 1, settings.nz+1])
            yy = npx.array([0, 500, 20000-500, 20000])
            k = npx.interp(vs.yt, yy, dd)
            k = npx.where(k>settings.nz, 0, k)  # land
            k = npx.floor(k)
        k = 0 * vs.kbot + 1
        k = update(k, at[:,0], 0)
        k = update(k, at[0, :], 0)

        vs.kbot = update(vs.kbot, at[...], k)

    @veros_routine
    def set_initial_conditions(self, state):

        vs = state.variables
        settings = state.settings


        temp = npx.ones(settings.nz)
        temp[:7] = 10
        temp[7:] = 30

        vs.temp = update(vs.temp, at[...],
                         temp[npx.newaxis, npx.newaxis, :, npx.newaxis])
        # try ssh anomally
        if False:
            psi0 = (vs.yt / 20000) * 9.8 * 10 - 9.8/2 * 10
            print(psi0)
            psi0 = psi0[npx.newaxis,:, npx.newaxis] + vs.psi
            print(npx.shape(vs.psi))
            vs.psi = update(vs.psi, at[...], psi0)


    @veros_routine
    def set_forcing(self, state):
        vs = state.variables

        settings = state.settings
        taux = allocate(state.dimensions, ("xu", "yt"))
        tauy = allocate(state.dimensions, ("xt", "yu"))
        tau0 = 0.02
        Rsq = 25e3**2
        speed = 0.2
        om = npx.pi * 2 / 40 / 3600
        x0, y0 = 0 * speed * vs.time + 320e3, speed * vs.time
        y0, x0 = 80e3, 320e3

        rsq = ((vs.xt-x0)**2)[:, npx.newaxis] + ((vs.yt-y0)**2)[npx.newaxis, :]
        t = tau0 * npx.exp(-(rsq/Rsq)) * npx.sin(vs.time * om)
        rsq = ((vs.xt-x0)**2)[:, npx.newaxis] + ((vs.yt-y0 - 10e3)**2)[npx.newaxis, :]
        t = t + tau0 * npx.exp(-(rsq/Rsq)) * npx.sin(vs.time * om)


        theta = npx.arctan2((vs.yt[npx.newaxis, :]-y0), (vs.xt[:, npx.newaxis]-x0))

        taux = -t * npx.sin(theta)
        tauy = t * npx.cos(theta)
        taux = 0 * taux
        tauy = t + 0 * tauy
        vs.surface_taux = update(vs.surface_taux, at[...], taux)
        vs.surface_tauy = update(vs.surface_tauy, at[...], tauy)

    @veros_routine
    def set_diagnostics(self, state):
        settings = state.settings
        diagnostics = state.diagnostics

        diagnostics["snapshot"].output_frequency = 3600

    @veros_routine
    def after_timestep(self, state):
        pass
