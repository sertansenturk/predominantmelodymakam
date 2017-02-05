#### predominantmelodymakam v1.2.2
 - Updated requirements file according to the change in 'pitchfilter' module.
 - Fixed a bug where the while loop fails directly when the audio input is very short.

#### predominantmelodymakam v1.2.1
 - Fixed a bug where the extract() method was not returning anything

#### predominantmelodymakam v1.2
 - Added the [pitchfilter](https://github.com/hsercanatli/pitchfilter) repository as a fallback if the Essetian PitchFilter does not work due to Essentia version problem (e.g. the official version for Ubuntu 14.04).
 - Added flake8 checking to Travis CI

#### predominantmelodymakam v1.1
 - Refactored the code to comply with PEP8

#### predominantmelodymakam v1.0
 - First public release
