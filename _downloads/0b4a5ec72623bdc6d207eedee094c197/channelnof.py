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

# globals:

JMKA_h = 4
JMKr_quad_bot = 1e-3
JMKkappaM_0 = 1e-3
JMKf0 = 0
JMKtau0 = 0.2
JMKidentifier = "channelnof"
JMKdt_mom = 30
JMKr_bot = 4e-3

from veros import VerosSetup, veros_routine
from veros.variables import allocate, Variable
from veros.distributed import global_min, global_max
from veros.core.operators import numpy as npx, update, at


class ChannelSetup(VerosSetup):
    """A model using cartesian coordinates in cyclic channel

    Wind forcing over a channel; no buoyancy

    """

    @veros_routine
    def set_parameter(self, state):
        settings = state.settings
        settings.identifier = JMKidentifier

        settings.nx, settings.ny, settings.nz = 4, 160, 45

        settings.dt_mom = JMKdt_mom
        settings.dt_tracer = settings.dt_mom
        settings.runlen = 3600 * 24 * 6

        settings.x_origin = 0.0
        settings.y_origin = 0.0

        settings.coord_degree = False
        settings.enable_cyclic_x = True

        settings.enable_neutral_diffusion = False

        settings.enable_hor_friction = True
        settings.enable_hor_diffusion = True
        settings.A_h = JMKA_h
        settings.K_h = settings.A_h
        settings.enable_hor_friction_cos_scaling = False
        settings.hor_friction_cosPower = 1

        settings.enable_bottom_friction = True
        settings.r_bot = JMKr_bot

        settings.enable_implicit_vert_friction = False
        settings.enable_explicit_vert_friction = True

        settings.kappaM_0 = JMKkappaM_0
        settings.kappaH_0 = JMKkappaM_0

        settings.enable_streamfunction = False

        settings.enable_idemix = False

        settings.eq_of_state_type = 1


    @veros_routine
    def set_grid(self, state):
        vs = state.variables
        settings = state.settings

        ddz = 50 / settings.nz
        vs.dxt = update(vs.dxt, at[...], 1000)
        vs.dyt = update(vs.dyt, at[...], 128)
        vs.dzt = update(vs.dzt, at[...], ddz)

    @veros_routine
    def set_coriolis(self, state):
        vs = state.variables
        settings = state.settings

        vs.coriolis_t = update(
            vs.coriolis_t, at[...], JMKf0
        )

    @veros_routine
    def set_topography(self, state):
        vs = state.variables
        settings = state.settings
        # depth of deepest cell.  0 is land,  1 is deepest
        # nz is shallowest..
        dd = npx.array([settings.nz+1, 1, 1, settings.nz+1])
        yy = npx.array([0, 500, 20000-500, 20000])
        k = npx.interp(vs.yt, yy, dd)
        k = npx.where(k>settings.nz, 0, k)  # land
        k = npx.floor(k)
        vs.kbot = vs.kbot * 0 + k.astype("int")[npx.newaxis, :]

    @veros_routine
    def set_initial_conditions(self, state):
        vs = state.variables
        settings = state.settings

        vs.temp = update(vs.temp, at[...], 10)
        taux = allocate(state.dimensions, ("xt", "yt")) + JMKtau0
        vs.surface_taux = update(vs.surface_taux, at[...], taux)

        # try ssh anomally
        if False:
            psi0 = (vs.yt / 20000) * 9.8 * 10 - 9.8/2 * 10
            print(psi0)
            psi0 = psi0[npx.newaxis,:, npx.newaxis] + vs.psi
            print(npx.shape(vs.psi))
            vs.psi = update(vs.psi, at[...], psi0)


    @veros_routine
    def set_forcing(self, state):
        pass

        #vs = state.variables
        # vs.forc_temp_surface = vs.t_rest * (vs.t_star - vs.temp[:, :, -1, vs.tau])

    @veros_routine
    def set_diagnostics(self, state):
        settings = state.settings
        diagnostics = state.diagnostics

        diagnostics["snapshot"].output_frequency = 3600


    @veros_routine
    def after_timestep(self, state):
        pass
