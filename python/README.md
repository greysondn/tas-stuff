# mario-paint-plotter
A simple scrap of python to do image plotting in Mario Paint on the SNES via
Bizhawk's TASStudio

# Original source

Was just going to be chucked into github and let to die. That's here:

https://github.com/greysondn/mario-paint-plotter

Specifically at commit d3276f1:

https://github.com/greysondn/mario-paint-plotter/tree/d3276f15f4b042d36234b4b9e839c2d44bf69206

This version is now the working/edited version. (You can tell I didn't plan this at all, can't you?)

# Environment
```
Python  3.7.2rc1
Pillow  8.0.1
Bizhawk 2.6.1

SNES - BSNES core, controller set to first port mouse, second port joypad

Matching ROM Image (GoodTools):
Mario Paint (JU) (!).smc
```

# How?
The code is largely self-documenting. Obnoxiously so in some cases, due to my own bad memory and obsessive note taking.

Run `plotter.py` under Python 3 for a REPL. Examine the code itself for a headache and stuff you can probably make use of with a little work.

The strange looking lines the plotter spits out and waits for you to see are copy/pastable directly into TASStudio.

# Why
I just really wanted to color a dinosaur, man.

The run this was built for has now been submitted; please see:  
http://tasvideos.org/7073S.html