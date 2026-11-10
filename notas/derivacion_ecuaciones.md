El voltaje que cae en un inductor debe ser igual segundo capacitor y $V_{L}=L\cdot \frac{di}{dt}$. 
$$
L\cdot \frac{dI}{dt}=-V_{2}
$$
haciendo nodos en el capacitor dos (Y recordando que $i_{c}=C\frac{dv}{dt}$, y tambien que la corriente sobre es $\frac{V}{R}$. 
$$
 I_{L}=C_{2} \frac{dV_{2}}{dt}-\frac{V_{1}}{R}+\frac{V_{2}}{R}
$$

Ahora haciendo lo mismo en $C_{1}$ 

$$
g(V_{1})=C_{1} \frac{dV_{1}}{dt}-\frac{1}{R}(V_{2}-V_{1})
$$

donde $g$ es la función característica del diodo de chua. 
ahora si defino $\alpha=\frac{C_{2}}{C_{1}}$, $\beta=\frac{C_{2}R^{2}}{L}$, $m_{0}=G_{a}R$ y $m_{1}=G_{b}R$ y cambio de variables a $x=\frac{V_{1}}{E}$,$y=\frac{V_{2}}{E}$ y $\tau=\frac{t}{RC_{2}}$, $z=R\frac{I_{3}}{E}$ 

$$
\begin{cases}
\dot{x}=\alpha(y-x-g(x)) \\
\dot{y}=x-y+z \\
\dot{z}=-\beta y
\end{cases}
$$

con 

$$
g(x)=m_{1}x+\frac{1}{2}(m_{0}-m_{1})[|x+1|-|x-1|]
$$