

import jax.numpy as jnp
import pandas as pd 
from diffrax import diffeqsolve, ODETerm, SaveAt, Tsit5

# Define constants 

a = -0.428
alpha = 9 
beta = 15 
epsilon = 0.125
psi =2 

def chua(t,state,b):
    x,y,z = state
    xdot = 9 * (y-x-(b*x +  -0.428*jnp.tanh(x*psi))) 
    ydot = x - y + z 
    zdot = -15 * y - 0.125 * z 
    return xdot, ydot, zdot

#SOLVER
term = ODETerm(chua)
solver = Tsit5()
ts= jnp.linspace(1300,1500,1000000)
saveat = SaveAt(ts=ts)

#LOOP 
bs = jnp.linspace(-0.375,-.5,2000)

xs = jnp.zeros([jnp.size(bs),jnp.size(ts)])
ys = jnp.zeros([jnp.size(bs),jnp.size(ts)])

for (n,b) in enumerate(bs):
    
    sol = diffeqsolve(term, solver, t0 =0, t1= int(ts[-1]),dt0 =0.01 , y0=(0.001,0,0.04),args=b,saveat=saveat,max_steps=1000000)
    
    xs.at[n,::].set(sol.ys[0])
    ys.at[n,::].set(sol.ys[1])

pd.DataFrame(xs).to_pickle('xs.pkl')
pd.DataFrame(ys).to_pickle('ys.pkl')