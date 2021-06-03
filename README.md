# NeonAI Mozilla TTS Plugin
[Mycroft](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins) compatible
TTS Plugin for Remote Mozilla Text-to-Speech. Note that this module requires a local or remote API server to be available.

# Configuration:

```yaml
tts:
    module: mozilla_remote
    mozilla_remote: {"api_url": "http://0.0.0.0:5002/api/tts"}
```