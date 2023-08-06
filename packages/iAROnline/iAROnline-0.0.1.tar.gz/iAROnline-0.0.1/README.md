iAROnline package
===========

Description
===========

Data sets, functions and scripts with examples to implement online estimation methods for the irregularly observed autoregressive (iAR) model [(Eyheramendy et al.(2018))](#1). The online learning algorithms implemented are: gradient descent (IAR_OGD), Newton-step (IAR-ONS) and Kalman filter recursions (IAR-OBR).

Contents
========

-  iAR Online Newton Step (iAR-ONS) [[1]](#2)
-  iAR Online Gradient Descent (iAR-OGD)[[2]](#2)
-  iAR Online Bayesian Regression (iAR-OBR) [[3]](#2)
-  iAR Online Bayesian Estimation (iAR-OBI) [[4]]

Instalation
=====================

Dependencies:

```
numpy
pandas
matplotlib
numba
iar
statistics
```

Install from PyPI using:

```
pip install iaronline
```

or clone this github and do:

```
python setup.py install --user
```

Examples
======================

-   iAROnline demo [here](https://github.com/felipeelorrieta/iAR/blob/master/examples/IAROnline_Demo.ipynb)

Authors
======================

-   Felipe Elorrieta (felipe.elorrieta@usach.cl) (Millennium Institute of Astrophysics and Universidad de Santiago de Chile)
-   Lucas Osses (Universidad de Santiago de Chile)


Acknowledgments
======================

The authors acknowledge support from the ANID – Millennium Science Initiative Program – ICN12_009 awarded to the Millennium Institute of Astrophysics MAS (www.astrofisicamas.cl) 

References
======================

<a id="1">[1]</a> Eyheramendy S, Elorrieta F, Palma W (2018). “An irregular discrete time series model to identify residuals with autocorrelation in astronomical light curves.” Monthly Notices of the Royal Astronomical Society, 481(4), 4311–4322. ISSN 0035-8711, doi: 10.1093/mnras/sty2487, https://academic.oup.com/mnras/article-pdf/481/4/4311/25906473/sty2487.pdf.

<a id="2">[2]</a> Elorrieta, F, Eyheramendy, S, Palma, W (2019). “Discrete-time autoregressive model for unequally spaced time-series observations.” A\& A, 627, A120. doi: 10.1051/00046361/201935560, https://doi.org/10.1051/0004-6361/201935560.

