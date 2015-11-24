# makampredominantmelody
Predominant melody extraction for makam music

Usage
=======
```python
from predominantmelodymakam.PredominantMelodyMakam import PredominantMelodyMakam
extractor = PredominantMelodyMakam()
results = extractor.run(audiofile)
```

Please refer to demo.ipynb for an interactive demo.

Installation
============

If you want to install alignednotemodels, it is recommended to install the package and dependencies into a virtualenv. In the terminal, do the following:

    virtualenv env
    source env/bin/activate
    python setup.py install

If you want to be able to edit files and have the changes be reflected, then install compmusic like this instead

    pip install -e .

Now you can install the rest of the dependencies:

    pip install -r requirements

Authors
-------
Hasan Sercan Atlı	hsercanatli@gmail.com
Sertan Senturk		contact@sertansenturk.com

Acknowledgements
------
We would like to thank Dr. Robert Grafias for allowing us to use his makam music collection (in this repository the recording with MBID: d2731692-626d-4a6d-9b67-a70c9e7b9745) in our research.

Reference
-------
Thesis