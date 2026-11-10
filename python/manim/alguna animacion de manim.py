from manimlib import * 
from scipy.integrate import odeint
from scipy.integrate import solve_ivp 
import numpy as np 

def f(x,a,b):
    return b * x + .5 *(a-b) * (np.abs(x+1)-np.abs(x-1))

def chua_circuit(t,state,alpha,beta,a,b):
    x,y,z = state
    dxdt = alpha * (y - x- f(x,a,b))
    dydt = x - y + z
    dzdt = -beta * y
    return [dxdt,dydt,dzdt]

def solve_chua_circuit(time,initial_condition,alpha=15.6,beta=28,a=-8/7,b=-5/7):
    solution = solve_ivp(
        chua_circuit,
        t_span  = (0,time),
        y0 = initial_condition,
        args = (alpha,beta,a,b),
        t_eval= np.arange(0,time,0.01),
        method='RK45'
    )
    return solution.y.T

class ChuaAttractor(ThreeDScene):
   def construct(self):
      # self.set_camera_orientation(phi=60*DEGREES, theta=10*DEGREES+ 3*PI/10)
      axes =ThreeDAxes(z_range=(-5,5),x_range=(-5,5),y_range=(-5,5))      
      self.add(axes)

      

      epsilon = 0.001
      evolution_time =50
      states =[
         [.1,.1,n*epsilon]
         for n in range(7)
      ]
      colors = color_gradient([RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE], len(states))
      curves=VGroup()


      for state, color in zip(states, colors):
         points = solve_chua_circuit(evolution_time, state)
         curve = VMobject().set_points_as_corners(points)
         curve.set_color(color,1)
         curves.add(curve)

      curves.set_stroke(width=1.5,opacity=0.9)
      dots = Group()

      for color in colors: 
         dot = Dot(color=color,radius=0.03)
         dots.add(dot)
      # dots = Group([Dot3D(color=RED,radius=0.05),Dot3D(color=BLUE,radius=0.05),Dot3D(color=GREEN,radius=0.05),Dot3D(color=PURPLE,radius=0.05),Dot3D(color=ORANGE,radius=0.05)])

      def update_dots(dots):
         for dot, curve in zip(dots, curves):
            dot.move_to(curve.get_end())

      dots.add_updater(update_dots)


      tails = VGroup()

      for dot in dots:
         tail = TracedPath(dot.get_center, time_traced=1.3,stroke_width=1.5,stroke_opacity=0.9,stroke_color=dot.get_color())
         tails.add(tail)

    #   self.begin_ambient_camera_rotation(rate=PI/25,about="theta")

      self.add(dots)
      self.add(tails)
      curves.set_opacity(0)
      self.frame.animate(PI/4,PI/4)
      self.play(*[ShowCreation(curve,rate_func=linear) for curve in curves], run_time=25)
    #   self.stop_ambient_camera_rotation()