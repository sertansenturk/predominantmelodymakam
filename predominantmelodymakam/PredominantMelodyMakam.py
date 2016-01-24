# -*- coding: utf-8 -*-
# Copyright 2014, 2015 Music Technology Group - Universitat Pompeu Fabra
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Affero General Public License v3.0 for more details.
#
# You should have received a copy of the GNU Affero General Public License v3.0 
# along with this program. If not, see http://www.gnu.org/licenses/
#
# If you are using this extractor please cite the following paper:
#
# Atlı, H. S., Uyar, B., Şentürk, S., Bozkurt, B., and Serra, X. (2014). Audio
# feature extraction for exploring Turkish makam music. In Proceedings of 3rd
# International Conference on Audio Technologies for Music and Media, Ankara,
# Turkey.

from essentia import Pool
from essentia import array as e_array
import essentia.standard as estd

from math import ceil
import numpy as np
from numpy import transpose

class PredominantMelodyMakam():
    _version = "0.6"
    _sourcetype = "mp3"
    _slug = "makampitch"

    def __init__(self, hopSize = 128, frameSize = 2048, binResolution = 7.5, minFrequency = 55, maxFrequency = 1760,
        magnitudeThreshold = 0, peakDistributionThreshold = 1.4, filterPitch = True, confidenceThreshold = 36, minChunkSize = 50):

        self.hopSize = hopSize    # default hopSize of PredominantMelody
        self.frameSize = frameSize  # default frameSize of PredominantMelody
        self.binResolution = binResolution  # ~1/3 Hc; recommended for makams
        self.minFrequency = minFrequency  # default minimum of PitchSalienceFunction
        self.maxFrequency = maxFrequency  # default maximum of PitchSalienceFunction
        self.magnitudeThreshold = magnitudeThreshold  # default of SpectralPeaks; 0 dB?
        self.peakDistributionThreshold = peakDistributionThreshold  # default in PitchContours is 0.9; we need higher in makams
        self.filterPitch = filterPitch  # call PitchFilter
        self.confidenceThreshold = confidenceThreshold  # default confidenceThreshold for pitchFilter
        self.minChunkSize = minChunkSize  # number of minimum allowed samples of a chunk in PitchFilter; ~145 ms with 128 sample hopSize & 44100 Fs

        self.sampleRate = 44100

    def getSettings(self):
      from essentia import __version__ as essentia_version
      citation = u"Atlı, H. S., Uyar, B., Şentürk, S., Bozkurt, B., and Serra, X. (2014). Audio feature extraction for exploring Turkish makam music. In Proceedings of 3rd International Conference on Audio Technologies for Music and Media, Ankara, Turkey."
      
      return {'hopSize': self.hopSize, 'frameSize': self.frameSize, 'pitchUnit': 'Hz', 
              'binResolution': self.binResolution, 'minFrequency': self.minFrequency, 
              'maxFrequency': self.maxFrequency, 'magnitudeThreshold': self.magnitudeThreshold, 
              'sampleRate':self.sampleRate, 'peakDistributionThreshold': self.peakDistributionThreshold, 
              'filterPitch': self.filterPitch, 'confidenceThreshold': self.confidenceThreshold, 
              'minChunkSize': self.minChunkSize, 'version':self._version, 'slug':self._slug, 
              'essentiaVersion': essentia_version, 'citation': citation}

    def run(self, fname):        
        run_windowing = estd.Windowing(zeroPadding = 3 * self.frameSize) # Hann window with x4 zero padding
        run_spectrum = estd.Spectrum(size=self.frameSize * 4)

        run_spectral_peaks = estd.SpectralPeaks(minFrequency=self.minFrequency,
                        maxFrequency = self.maxFrequency,
                        sampleRate = self.sampleRate,
                        magnitudeThreshold = self.magnitudeThreshold,
                        orderBy = 'magnitude')

        # convert unit to cents, PitchSalienceFunction takes 55 Hz as the default reference
        run_pitch_salience_function = estd.PitchSalienceFunction(binResolution=self.binResolution) 
        run_pitch_salience_function_peaks = estd.PitchSalienceFunctionPeaks(binResolution=self.binResolution,
                        minFrequency=self.minFrequency,
                        maxFrequency = self.maxFrequency)
        run_pitch_contours = estd.PitchContours(hopSize=self.hopSize,
                        binResolution=self.binResolution,
                        peakDistributionThreshold = self.peakDistributionThreshold)

        if self.filterPitch:
            run_pitch_filter = estd.PitchFilter(confidenceThreshold=self.confidenceThreshold,
                                                minChunkSize=self.minChunkSize)

        pool = Pool()

        # load audio and eqLoudness
        audio = estd.MonoLoader(filename = fname)() # MonoLoader resamples the audio signal to 44100 Hz by default
        audio = estd.EqualLoudness()(audio)

        for frame in estd.FrameGenerator(audio,frameSize=self.frameSize, hopSize=self.hopSize):
            frame = run_windowing(frame)
            spectrum = run_spectrum(frame)
            peak_frequencies, peak_magnitudes = run_spectral_peaks(spectrum)
            salience = run_pitch_salience_function(peak_frequencies, peak_magnitudes)
            salience_peaks_bins, salience_peaks_contourSaliences = run_pitch_salience_function_peaks(salience)
            if not np.size(salience_peaks_bins):
                    salience_peaks_bins = np.array([0])
            if not np.size(salience_peaks_contourSaliences):
                    salience_peaks_contourSaliences = np.array([0])

            pool.add('allframes_salience_peaks_bins', salience_peaks_bins)
            pool.add('allframes_salience_peaks_contourSaliences', salience_peaks_contourSaliences)

        # post-processing: contour tracking
        contours_bins, contours_contourSaliences, contours_start_times, duration = run_pitch_contours(
                        pool['allframes_salience_peaks_bins'],
                        pool['allframes_salience_peaks_contourSaliences'])

        # run the simplified contour selection
        [pitch, pitch_salience] = self.ContourSelection(contours_bins,contours_contourSaliences,contours_start_times,duration)

        # cent to Hz conversion
        pitch = e_array([0. if p == 0 else 55.*(2.**(((self.binResolution*(p)))/1200)) for p in pitch])
        pitch_salience = e_array(pitch_salience)

        # pitch filter
        if self.filterPitch:
            pitch = run_pitch_filter(pitch, pitch_salience)

        # generate time stamps
        time_stamps = [s*self.hopSize/float(self.sampleRate) for s in xrange(0,len(pitch))]

        # [time pitch salience] matrix
        out = np.transpose(np.vstack((time_stamps, pitch.tolist(), pitch_salience.tolist())))
        out = out.tolist()

        # settings
        settings = self.getSettings()
        settings.update({'source': fname})

        return {'pitch': out, 'settings': settings}

    def ContourSelection(self,pitchContours,contourSaliences,startTimes,duration):
        sampleRate = self.sampleRate

        hopSize = self.hopSize

        # number in samples in the audio
        numSamples = int(ceil((duration * sampleRate)/hopSize))

        #Start points of the contours in samples
        startSamples = [int(round(startTimes[i] * sampleRate/float(hopSize))) for i in xrange(0,len(startTimes))]

        pitchContours_noOverlap = []
        startSamples_noOverlap = []
        contourSaliences_noOverlap = []
        lens_noOverlap = []
        while pitchContours: # terminate when all the contours are checked
            #print len(pitchContours)

            # get the lengths of the pitchContours
            lens = [len(k) for k in pitchContours]

            # find the longest pitch contour
            long_idx = lens.index(max(lens))

            # pop the lists related to the longest pitchContour and append it to the new list
            pitchContours_noOverlap.append(pitchContours.pop(long_idx))
            contourSaliences_noOverlap.append(contourSaliences.pop(long_idx))
            startSamples_noOverlap.append(startSamples.pop(long_idx))
            lens_noOverlap.append(lens.pop(long_idx))

            # accumulate the filled samples
            acc_idx = range(startSamples_noOverlap[-1], startSamples_noOverlap[-1] + lens_noOverlap[-1])

            # remove overlaps
            [startSamples, pitchContours, contourSaliences] = self.RemoveOverlaps(startSamples, pitchContours, contourSaliences, lens, acc_idx)

        # accumulate pitch and salience
        pitch = np.array([0.] * (numSamples))
        salience = np.array([0.] * (numSamples))
        for i in xrange(0,len(pitchContours_noOverlap)):
            startSample = startSamples_noOverlap[i]
            endSample = startSamples_noOverlap[i] + len(pitchContours_noOverlap[i])

            try:
                pitch[startSample:endSample] = pitchContours_noOverlap[i]
                salience[startSample:endSample] = contourSaliences_noOverlap[i]

            except ValueError:
                print "The last pitch contour exceeds the audio length. Trimming..."

                pitch[startSample:] = pitchContours_noOverlap[i][:len(pitch)-startSample]
                salience[startSample:] = contourSaliences_noOverlap[i][:len(pitch)-startSample]

        return pitch, salience

    def RemoveOverlaps(self, startSamples, pitchContours, contourSaliences, lens, acc_idx):
        # remove overlaps
        rmv_idx = []
        for i in xrange(0, len(startSamples)):
            #print '_' + str(i)
            # create the sample index vector for the checked pitch contour
            curr_samp_idx = range(startSamples[i], startSamples[i] + lens[i])

            # get the non-overlapping samples
            curr_samp_idx_noOverlap = (list(set(curr_samp_idx) - set(acc_idx)))

            if curr_samp_idx_noOverlap:
                temp = min(curr_samp_idx_noOverlap)
                keep_idx = range(temp-startSamples[i], (max(curr_samp_idx_noOverlap)-startSamples[i])+1)

                # remove all overlapping values
                pitchContours[i] = np.array(pitchContours[i])[keep_idx]
                contourSaliences[i] = np.array(contourSaliences[i])[keep_idx]
                # update the startSample
                startSamples[i] = temp
            else: # totally overlapping
                rmv_idx.append(i)

        # remove totally overlapping pitch contours
        rmv_idx = sorted(rmv_idx, reverse=True)
        for r in rmv_idx:
            pitchContours.pop(r)
            contourSaliences.pop(r)
            startSamples.pop(r)

        return startSamples, pitchContours, contourSaliences
