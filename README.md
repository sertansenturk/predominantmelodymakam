[![GitHub version](https://badge.fury.io/gh/sertansenturk%2Fpredominantmelodymakam.svg)](https://badge.fury.io/gh/sertansenturk%2Fpredominantmelodymakam) [![Build Status](https://travis-ci.org/sertansenturk/predominantmelodymakam.svg?branch=master)](https://travis-ci.org/sertansenturk/predominantmelodymakam) [![Code Climate](https://codeclimate.com/github/sertansenturk/predominantmelodymakam/badges/gpa.svg)](https://codeclimate.com/github/sertansenturk/predominantmelodymakam) [![DOI](https://zenodo.org/badge/21104/sertansenturk/predominantmelodymakam.svg)](https://zenodo.org/badge/latestdoi/21104/sertansenturk/predominantmelodymakam) [![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-ff69b4.svg)](http://www.gnu.org/licenses/agpl-3.0)

# predominantmelodymakam
Predominant melody extraction for makam music

This repository hosts the the implementation of the predominant melody extraction proposed for makam music in:

> Atlı, H. S., Uyar, B., Şentürk, S., Bozkurt, B., and Serra, X. (2014). Audio feature extraction for exploring Turkish makam music. In Proceedings of 3rd International Conference on Audio Technologies for Music and Media, pages 142–153, Ankara, Turkey.

If you are using this extractor please cite the above paper. 

The extractor is based on the methodology by [2]. The contour selection step in [2] is trained on the specfic characteristics of Western pop music and jazz. We remove this step and use a simplified contour selection step by selecting the longest contour at each time instance and discarding all other contours. Then we use the method proposed in [3] to remove the erroneous pitch estimations and correct octave errors.
	
Usage
=======
```python
from predominantmelodymakam.predominantmelodymakam import PredominantMelodyMakam
extractor = PredominantMelodyMakam()
results = extractor.run(audiofile)
```

Please refer to demo.ipynb for an interactive demo.

Installation
============

If you want to install the repository, it is recommended to install the package and dependencies into a virtualenv. In the terminal, do the following:

    virtualenv env
    source env/bin/activate
    python setup.py install

If you want to be able to edit files and have the changes be reflected, then install the repo like this instead:

    pip install -e .
    
Now you can install the rest of the dependencies:

    pip install -r requirements

The algorithm uses several modules in Essentia. Follow the [instructions](essentia.upf.edu/documentation/installing.html) to install the library. Then you should link the python bindings of Essentia in the virtual environment:

    ln -s /usr/local/lib/python2.7/dist-packages/essentia env/lib/python2.7/site-packages

Authors
-------
Hasan Sercan Atlı	hsercanatli@gmail.com  
Sertan Senturk		contact@sertansenturk.com

License
------
The source code hosted in this repository is licenced under [Affero GPL version 3](https://www.gnu.org/licenses/agpl-3.0.en.html). 

The extracted predominant melody and the figure in this repository are licenced under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).

Acknowledgements
------
We would like to thank Dr. Robert Garfias for allowing us to use [his makam music collection](https://eee.uci.edu/programs/rgarfias/films.html) in our research (in this repository the recording with MBID: [d2731692-626d-4a6d-9b67-a70c9e7b9745](http://musicbrainz.org/recording/d2731692-626d-4a6d-9b67-a70c9e7b9745)).

References
-------
[1] _Atlı, H. S., Uyar, B., Şentürk, S., Bozkurt, B., and Serra, X. (2014). Audio feature extraction for exploring Turkish makam music. In Proceedings of 3rd International Conference on Audio Technologies for Music and Media, Ankara, Turkey._   
[2] _Salamon, J., Gómez, E. (2012). "Melody Extraction from Polyphonic Music Signals using Pitch Contour Characteristics", IEEE Transactions on Audio, Speech and Language Processing, 20(6):1759-1770_   
[3] _Bozkurt, B. (2008). "An Automatic Pitch Analysis Method for Turkish Maqam Music," Journal of New Music Research. 37(1):1-13._
