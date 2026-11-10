import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import jax.numpy as jnp
from diffrax import diffeqsolve, ODETerm, SaveAt, Tsit5
import pandas as pd


# FUNCION
def chua2(t, state, args):
    x, y, z = state
    beta = args
    alpha = 15.6
    m0 = -8 / 7
    m1 = -5 / 7
    a = 10
    xdot = alpha * (
        y
        - x
        - (
            m1 * x
            + (m0 - m1)
            / 2
            * (1 / a)
            * (jnp.log(jnp.cosh(a * x + a)) - jnp.log(jnp.cosh(a * x - a)))
        )
    )
    ydot = x - y + z
    zdot = -beta * y
    return xdot, ydot, zdot


# SOLVER:
term = ODETerm(chua2)
solver = Tsit5()

ts = jnp.linspace(1000, 1150, 60000)
saveat = SaveAt(ts=ts)

# LOOP
betas = jnp.arange(22.8,38, 0.005)
xs = jnp.empty([np.size(betas), np.size(ts)])
ys = jnp.empty([np.size(betas), np.size(ts)])
# se selecciona un valor en particular con xs[bs=0,::]

# RUN LOOP
for n, beta in enumerate(betas):
    sol = diffeqsolve(
        terms=term,
        solver=solver,
        t0=0,
        t1=int(ts[-1]),
        dt0=0.01,
        y0=(0.001, 0, 0.04),
        args=(beta),
        saveat=saveat,
        max_steps=1000000,
    )

    xs = xs.at[n, ::].set(sol.ys[0])
    ys = ys.at[n, ::].set(sol.ys[1])

    print(f"Loop:{n} de {np.size(betas)} completado")
    if n % 100 == 0:
        xspd = pd.DataFrame(xs)
        yspd = pd.DataFrame(ys)

        yspd.to_pickle("ys2_autosave.pkl")
        xspd.to_pickle("xs2_autosave.pkl")
        print(f"Guardado de seguridad completado en n={n} y beta ={beta}")


xsspd = pd.DataFrame(xs)
ysspd = pd.DataFrame(ys)

ysspd.to_pickle("ys2.pkl")
xsspd.to_pickle("xs2.pkl")
