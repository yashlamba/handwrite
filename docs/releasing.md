# Releasing Handwrite

Handwrite is released from `main`. The version tag must exactly match the version
in `pyproject.toml`; tags use `0.4.0`, not `v0.4.0`.

1. Update `project.version` in `pyproject.toml` and refresh the lockfile:

   ```console
   uv lock
   ```

2. Merge the version change into `main` and wait for the test and documentation
   workflows to pass.

3. Create and push an annotated tag from the release commit:

   ```console
   git tag -a 0.4.0 -m "Release 0.4.0"
   git push origin 0.4.0
   ```

The tag starts the release workflow. It validates the tag, builds the wheel and
source distribution, publishes both to PyPI, and creates a GitHub Release with
the same artifacts and generated release notes.

If the workflow fails before publication, fix the problem and rerun it. Never
move or reuse a tag after its version has been published to PyPI.
