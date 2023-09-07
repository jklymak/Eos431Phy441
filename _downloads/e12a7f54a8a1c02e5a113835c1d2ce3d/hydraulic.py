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
from veros.tools.setup import get_stretched_grid_steps


class ChannelSetup(VerosSetup):
    """A model using cartesian coordinates in cyclic channel

    Wind forcing over a channel; no buoyancy

    """

    @veros_routine
    def set_parameter(self, state):
        settings = state.settings
        settings.identifier = "hydraulic"

        settings.nx, settings.ny, settings.nz = 200, 4, 90

        settings.dt_mom = 20
        settings.dt_tracer = settings.dt_mom
        settings.runlen = 3600 * 60

        settings.x_origin = 0.0
        settings.y_origin = 0.0

        settings.coord_degree = False
        settings.enable_cyclic_x = False

        settings.enable_neutral_diffusion = False

        settings.enable_hor_friction = True
        settings.enable_hor_diffusion = True
        settings.A_h = 10
        settings.K_h = settings.A_h
        settings.enable_hor_friction_cos_scaling = False
        settings.hor_friction_cosPower = 1

        settings.enable_quadratic_bottom_friction = True
        settings.r_quad_bot = 1e-3

        settings.enable_implicit_vert_friction = True
        settings.enable_explicit_vert_friction = False

        settings.kappaM_0 = 4e-4
        settings.kappaH_0 = 4e-4

        settings.enable_streamfunction = False

        settings.enable_idemix = False

        settings.eq_of_state_type = 1

    @veros_routine(dist_safe=False, local_variables=['dxt', 'dyt', 'dzt'])
    def set_grid(self, state):
        vs = state.variables
        settings = state.settings

        ddz = 200 / settings.nz

        if False:
            vs.dxt = update(vs.dxt, at[...], 400)
            if True:
                for i in range(int(settings.nx / 3), -1, -1):
                    vs.dxt = update(vs.dxt, at[i], vs.dxt[i+1] * 1.05)
                for i in range(int(2*settings.nx / 3)-1, settings.nx+4):
                    vs.dxt = update(vs.dxt, at[i], vs.dxt[i-1] * 1.05)

        dx = get_stretched_grid_steps(102-25, 150e3, 400)
        vs.dxt = update(vs.dxt, at[...], npx.hstack((dx[::-1], npx.ones(50)*400, dx)))
        vs.dyt = update(vs.dyt, at[...], 1000)
        vs.dzt = update(vs.dzt, at[...], ddz)

    @veros_routine
    def set_coriolis(self, state):
        vs = state.variables
        # settings = state.settings
        vs.coriolis_t = update(
            vs.coriolis_t, at[...], 0e-4
        )

    @veros_routine
    def set_topography(self, state):
        vs = state.variables
        # depth of deepest cell.  0 is land,  1 is deepest
        # nz is shallowest..
        vs.kbot = update(vs.kbot, at[...], 1)

        kbot = npx.ones_like(vs.kbot[:, 0])
        x = vs.xt
        x = x - npx.mean(x)
        kbot += npx.floor(35*npx.exp(-(x/25000)**2)).astype("int")
        for j in range(state.settings.ny+1):
            vs.kbot = update(vs.kbot, at[:, j], kbot)
        vs.kbot = update(vs.kbot, at[:, 0], 0)
        vs.kbot = update(vs.kbot, at[0, :], 0)

    @veros_routine
    def set_initial_conditions(self, state):
        vs = state.variables
        settings = state.settings
        nx = settings.nx
        tbot = 10
        ttop = 14
        inx = npx.nonzero(vs.xt > npx.mean(vs.xt))[0]
        with settings.unlock():
            settings.x_origin = -npx.mean(vs.xt)
            vs.xt = update(vs.xt, at[...], vs.xt+settings.x_origin)
            vs.xu = update(vs.xu, at[...], vs.xu+settings.x_origin)

        vs.temp = update(vs.temp, at[:inx[0], :, :, :], tbot)
        vs.temp = update(vs.temp, at[inx[0]:, :, :, :], ttop)

        vs.temp = update(vs.temp, at[:, :, :30, :], tbot)
        vs.temp = update(vs.temp, at[:, :, settings.nz-30:, :], ttop)


    @veros_routine
    def set_forcing(self, state):
        pass
        #        vs = state.variables
        # vs.forc_temp_surface = vs.t_rest * (vs.t_star - vs.temp[:, :, -1, vs.tau])

    @veros_routine
    def set_diagnostics(self, state):
        settings = state.settings
        diagnostics = state.diagnostics

        diagnostics["snapshot"].output_frequency = 7200


    @veros_routine
    def after_timestep(self, state):
        pass
