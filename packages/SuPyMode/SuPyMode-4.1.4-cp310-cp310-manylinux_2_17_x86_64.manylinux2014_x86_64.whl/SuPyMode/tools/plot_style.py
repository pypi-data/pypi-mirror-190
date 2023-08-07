#!/usr/bin/env python
# -*- coding: utf-8 -*-

beta = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Propagation constant'
}

index = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Effective refraction index'
}

field = {
    "show_legend": False,
    "x_label": r'X-Direction [$\mu m$]',
    "y_label": r'Y-direction [$\mu m$]',
    "equal": True
}

adiabatic = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": r'Adiabatic criterion',
    "y_scale": 'log',
    "y_limits": [1e-5, None]
}


coupling = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Mode coupling'    
}