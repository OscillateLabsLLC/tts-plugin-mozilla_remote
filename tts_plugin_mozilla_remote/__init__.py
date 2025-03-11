# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc., Oscillate Labs LLC
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# Mike Gray
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
from os import PathLike
from typing import Literal, Optional, Union, Dict, Any, Type, Tuple

import requests
from ovos_plugin_manager.templates.tts import TTS, TTSValidator

from .version import __version__

__all__ = ["MozillaRemoteTTS", "__version__"]


class MozillaRemoteTTS(TTS):
    """
    Mozilla/Coqui Remote TTS Plugin

    Args:
        config (dict): The configuration for the plugin
        audio_ext (str): The audio file extension to use
    """

    CONFIG_DEFAULTS = {"log_timestamps": False}

    def __init__(self, config: Optional[Dict[str, Any]] = None, audio_ext: str = "wav"):
        config = config if config is not None else self.CONFIG_DEFAULTS.copy()
        super().__init__(config=config, validator=RemoteMozillaTTSValidator(self), audio_ext=audio_ext)
        self.config = config
        self.log_timestamps = False
        self.url = self.config.get("api_url", None) or self.config.get("url")
        if not self.url:
            raise ValueError("TTS URL not configured. Set 'url' or 'api_url' in config.")

    def get_tts(
        self, sentence: str, wav_file: Union[str, PathLike], lang: Optional[str] = None, voice: Optional[str] = None
    ) -> Tuple[Optional[Union[str, PathLike]], None]:
        """
        Get the TTS for a sentence

        Args:
            sentence (str): The sentence to convert to speech
            wav_file (Union[str, PathLike]): The file to save the audio to
            lang (Optional[str]): The language to use
            voice (Optional[str]): The voice to use

        Returns:
            Tuple[Union[str, PathLike], None]: The file path and None (plugin does not support phoneme generation)

        Raises:
            ValueError: If the URL is not configured or response is invalid
            requests.RequestException: If the request fails
        """
        sentence = self.remove_ssml(self.format_speak_tags(sentence, False))
        if not sentence:
            return None, None

        params = {"text": sentence}
        if voice:
            params["voice"] = voice.replace(" ", "%20")
        if lang:
            params["language_id"] = lang

        resp = requests.get(self.url, params=params, timeout=15)
        resp.raise_for_status()
        wav_data = resp.content

        if not wav_data:
            raise ValueError("Empty response from TTS API")
        if not isinstance(wav_data, bytes):
            raise ValueError(f"Invalid response type from TTS API: {type(wav_data)}")

        with open(wav_file, "wb") as f:
            f.write(wav_data)
        return wav_file, None


class RemoteMozillaTTSValidator(TTSValidator):
    """
    Validator for the Mozilla/Coqui Remote TTS Plugin
    """

    def __init__(self, tts: MozillaRemoteTTS):
        super().__init__(tts)
        self.tts = tts  # Keep reference to original TTS object

    def validate_connection(self) -> Literal[True]:
        """
        Validate the connection

        Returns:
            Literal[True]: Always returns True if validation succeeds

        Raises:
            ValueError: If URL is not configured
            requests.RequestException: If connection test fails
        """
        url = self.tts.url

        resp = requests.get(f"{url}&text=hi", timeout=3)
        resp.raise_for_status()
        return True

    def get_tts_class(self) -> Type[TTS]:
        """
        Get the TTS class

        Returns:
            Type[TTS]: The TTS class
        """
        return self.tts.__class__
