#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# example program for kaldi live nnet3 chain online decoding
#
# configured for embedded systems (e.g. an rpi3) with models
# installed in /opt/kaldi/model/
#

#Adapted and ported to Python3

import traceback
import logging
import datetime

from time                  import time
from nltools               import misc
from nltools.pulserecorder import PulseRecorder
from nltools.vad           import VAD, BUFFER_DURATION
from nltools.asr           import ASR, ASR_ENGINE_NNET3
from optparse              import OptionParser


#
# init
#

PROC_TITLE                       = 'kaldi_live_demo'


DEFAULT_ACOUSTIC_SCALE           = 1.0
DEFAULT_BEAM                     = 5.0
DEFAULT_FRAME_SUBSAMPLING_FACTOR = 3

STREAM_ID                        = 'mic'

source         = ""
volume         = 150
aggressiveness = 2
model_dir      = 'de_400k_nnet3chain_tdnn1f_2048_sp_bi.tar/de_400k_nnet3chain_tdnn1f_2048_sp_bi/de_400k_nnet3chain_tdnn1f_2048_sp_bi'

misc.init_app(PROC_TITLE)

print("Kaldi live demo V0.2")

#
# pulseaudio recorder
#

rec = PulseRecorder (source_name=source, volume=volume)

#
# VAD
#

vad = VAD(aggressiveness=aggressiveness)

#
# ASR
#

print "Loading model from %s ..." % model_dir

asr = ASR(engine = ASR_ENGINE_NNET3, model_dir = model_dir,
          kaldi_beam = DEFAULT_BEAM, kaldi_acoustic_scale = DEFAULT_ACOUSTIC_SCALE,
          kaldi_frame_subsampling_factor = DEFAULT_FRAME_SUBSAMPLING_FACTOR)


#
# main
#

rec.start_recording()

print("Please speak.")

while True:

    samples = rec.get_samples()

    audio, finalize = vad.process_audio(samples)

    if not audio:
        continue

    logging.debug ('decoding audio len=%d finalize=%s audio=%s' % (len(audio), repr(finalize), audio[0].__class__))

    user_utt, confidence = asr.decode(audio, finalize, stream_id=STREAM_ID)

    print("\r%s                     " % user_utt)

    if finalize:
        print()
