# Contributing to tts-plugin-mozilla_remote

Thanks for your interest in contributing!

**Note:** This project is in **Security Fixes Only** status. We accept:

- Security vulnerability fixes
- Critical bug fixes
- Dependency updates for security

We are **not** accepting new features or enhancements at this time.

## Development Setup

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- A running Mozilla TTS or Coqui TTS API server (for integration testing)
  - Internally, we use the Coqui TTS API server in a container for testing.

### Getting Started

```bash
git clone https://github.com/OscillateLabsLLC/tts-plugin-mozilla_remote
cd tts-plugin-mozilla_remote

# Install dependencies
uv sync
```

## Common Commands

```bash
# Run tests
uv run pytest tests/test_mtts.py

# Run tests with JUnit output
uv run pytest tests/test_mtts.py --junitxml=tests/tts-test-results.xml
```

## Security Vulnerabilities

If you discover a security vulnerability, please:

1. **Do not** open a public issue
2. Email mike@oscillatelabs.net with details
3. Include steps to reproduce if possible
4. Allow time for a patch before public disclosure

## Pull Requests

For security fixes and critical bugs:

1. Create a feature branch: `git checkout -b fix/security-issue`
2. Make your changes and add tests where applicable
3. Run `uv run pytest tests/test_mtts.py` to ensure all tests pass
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `fix:`, `chore:`)
5. Push to your fork
6. Open a pull request with a clear description of the fix

**Accepted prefixes for this project:**

- `fix:` - Bug fixes and security patches
- `chore:` - Dependency updates and maintenance
- `docs:` - Documentation updates
- `test:` - Test additions or modifications

## Release Process

This project uses [release-please](https://github.com/googleapis/release-please) for automated versioning:

1. Create commits using conventional commit messages
2. Release-please creates a PR with version bump and changelog
3. When the PR is merged, a release is created automatically
4. Package is published to PyPI

## License

By contributing, you agree that your contributions will be licensed under the BSD 3-Clause License.
