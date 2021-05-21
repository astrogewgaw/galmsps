# galmsps

[![Code style: black][black-badge]][black]

this is my own copy of the [**galactic MSPs database**][webcat], which is maintained as a simple plain text file [**here**][txtcat]. the code to scrap the database is in the [**scrap.py**](scrap.py) file, and the database itself (in all its JSONic glory) is in the [**galmsps.json**](galmsps.json) file. the data is updated on every Friday, at midnight (in UTC time). this repository will eventually power the [**koshka**][koshka] package, which aims to make accessing all pulsar and radio transient related catalogues easier.

[black]: https://github.com/psf/black
[koshka]: https://github.com/astrogewgaw/koshka
[webcat]: http://astro.phys.wvu.edu/GalacticMSPs/
[txtcat]: http://astro.phys.wvu.edu/GalacticMSPs/GalacticMSPs.txt
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
