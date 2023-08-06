from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'iAROnline',
    version='0.0.1',
    description='Online estimation methods for the irregularly observed autoregressive (iAR) model',
    long_description='Data sets, functions and scripts with examples to implement online estimation methods for the irregularly observed autoregressive (iAR) model (Eyheramendy et al.(2018) <doi:10.1093/mnras/sty2487>). The online learning algorithms implemented are: gradient descent (IAR_OGD), Newton-step (IAR-ONS) and Kalman filter recursions (IAR-OBR).',
    url='https://github.com/felipeelorrieta/Onlineiar',
    author='Felipe Elorrieta',
    author_email='<felipe.elorrieta@usach.cl>',
    license='MIT',
    classifiers=classifiers,
    keywords = ['irregulary observed time series','autoregressive','online estimation methods'],
    packages=find_packages(),
    install_requires=['numpy','pandas','matplotlib','numba','iar','statistics'],
    package_dir={'iAROnline':'iAROnline'},
    package_data={"":["../data/*.csv"]},
    zip_safe=False)
