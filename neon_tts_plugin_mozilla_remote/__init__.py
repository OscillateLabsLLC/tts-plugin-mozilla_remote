# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests

from ovos_plugin_manager.templates.tts import TTS, TTSValidator


class MozillaRemoteTTS(TTS):

    def __init__(self, lang="en-us", config=None):
        super().__init__(lang, config,
                         RemoteMozillaTTSValidator(self),
                         audio_ext="wav")
        self.url = self.config.get("api_url") or \
            self.config.get("url") or "https://mtts.2022.us/api/tts"  # mycroft-core compat

    def get_tts(self, sentence, wav_file, lang=None):
        sentence = self.remove_ssml(self.format_speak_tags(sentence, False))
        if not sentence:
            return None, None
        params = {"text": sentence}
        wav_data = requests.get(self.url, params=params).content
        with open(wav_file, "wb") as f:
            f.write(wav_data)
        return wav_file, None


class RemoteMozillaTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(RemoteMozillaTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_dependencies(self):
        pass

    def validate_connection(self):
        # TODO
        pass

    def get_tts_class(self):
        return self.tts.__class__
