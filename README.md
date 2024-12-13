# Mozilla/Coqui TTS Plugin for OVOS or Neon

TTS Plugin for Remote Mozilla or Coqui Text-to-Speech. Note that this module requires a local or remote API server to be available.

Looking for a Coqui plugin that also loads the model? Check out [ovos-tts-plugin-coqui](https://github.com/OpenVoiceOS/ovos-tts-plugin-coqui)

## Configuration

using mycroft.conf

```json
"tts": {
    "module": "mozilla_remote",
    "mozilla_remote": {
      "api_url": "http://0.0.0.0:5002/api/tts"
    }
}
```

using neon.yaml

```yaml
tts:
  module: mozilla_remote
  mozilla_remote: { "api_url": "http://0.0.0.0:5002/api/tts" }
```

## Usage

Standalone usage

```python
from tts_plugin_mozilla_remote import MozillaRemoteTTS

engine = MozillaRemoteTTS(config={"api_url": "http://0.0.0.0:5002/api/tts"})
engine.get_tts("hello world", "test.wav")
```
