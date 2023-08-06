"""
Data sets, functions and scripts with examples to implement online estimation methods for the irregularly observed autoregressive (iAR) model (Eyheramendy et al.(2018) <doi:10.1093/mnras/sty2487>). The online learning algorithms implemented are: gradient descent (IAR_OGD), Newton-step (IAR-ONS) and Kalman filter recursions (IAR-OBR).  
https://github.com/felipeelorrieta/Onlineiar
"""

__version__ = '1.0.0'

from .methods import IAR_OBI,IAR_OBR,IAR_OGD,IAR_ONS,IARg_OGD,IARg_ONS,update_ONS,update_OGD
