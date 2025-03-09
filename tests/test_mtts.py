# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc. Oscillate Labs LLC
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions
#    and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#    and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tts_plugin_mozilla_remote import MozillaRemoteTTS, RemoteMozillaTTSValidator


class TestMozilla(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        tts_url = os.getenv("TTS_URL") or "https://mtts.2022.us"
        cls.mTTS = MozillaRemoteTTS(config={"api_url": tts_url})

    @classmethod
    def tearDownClass(cls) -> None:
        # Clean up all test files
        test_dir = os.path.dirname(__file__)
        for test_file in ["test.wav", "test2.wav"]:
            try:
                os.remove(os.path.join(test_dir, test_file))
            except FileNotFoundError:
                pass

        try:
            if hasattr(cls.mTTS, "playback") and cls.mTTS.playback is not None:
                cls.mTTS.playback.stop()
                cls.mTTS.playback.join()
        except (AttributeError, RuntimeError):
            pass

    def test_speak_no_params(self):
        out_file = os.path.join(os.path.dirname(__file__), "test.wav")
        file, _ = self.mTTS.get_tts("Hello.", out_file)
        self.assertEqual(file, out_file)

    def test_empty_speak(self):
        out_file = os.path.join(os.path.dirname(__file__), "test2.wav")
        file, _ = self.mTTS.get_tts("</speak>Hello.", out_file)
        self.assertFalse(os.path.isfile(out_file))

    def test_pathlike_output(self):
        """Test that PathLike objects work for output files."""
        out_file = Path(os.path.dirname(__file__)) / "test.wav"
        file, _ = self.mTTS.get_tts("Hello.", out_file)
        self.assertEqual(file, out_file)

    def test_no_url_configured(self):
        """Test that proper error is raised when URL is not configured."""
        with self.assertRaisesRegex(ValueError, "TTS URL not configured"):
            MozillaRemoteTTS(config={"url": "", "api_url": ""})

    def test_invalid_response_type(self):
        """Test handling of invalid response types."""
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.content = {"error": "Invalid response"}  # Not bytes
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with self.assertRaisesRegex(ValueError, "Invalid response type"):
                self.mTTS.get_tts("Hello.", "test.wav")

    def test_empty_response(self):
        """Test handling of empty responses."""
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.content = b""  # Empty bytes
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with self.assertRaisesRegex(ValueError, "Empty response"):
                self.mTTS.get_tts("Hello.", "test.wav")

    def test_voice_param_encoding(self):
        """Test that voice parameter is properly URL encoded."""
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.content = b"test"
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            self.mTTS.get_tts("Hello.", "test.wav", voice="Test Voice")

            # Verify the space was encoded
            _, kwargs = mock_get.call_args
            self.assertEqual(kwargs["params"]["voice"], "Test%20Voice")


if __name__ == "__main__":
    unittest.main()
