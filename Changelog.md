#### predominantmelodymakam v1.3.0
 - Added Python 3 support (contribution by Oriol Romani: https://github.com/sertansenturk/predominantmelodymakam/pull/10)

#### predominantmelodymakam v1.2.2
 - Corrected the name of the 'pitchfilter' package in the requirements file.
 - Fixed a bug where the pitch contour selection step fails, when the audio input is very short.

#### predominantmelodymakam v1.2.1
 - Fixed a bug where the extract() method was not returning anything

#### predominantmelodymakam v1.2
 - Added the [pitchfilter](https://github.com/hsercanatli/pitchfilter) repository as a fallback if the Essentia PitchFilter does not work due to Essentia version problem (e.g. the official version for Ubuntu 14.04).
 - Added flake8 checking to Travis CI

#### predominantmelodymakam v1.1
 - Refactored the code to comply with PEP8

#### predominantmelodymakam v1.0
 - First public release
