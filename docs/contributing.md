# Development

## Linux

1. Install Potrace using apt

   ```console
   sudo apt-get install potrace
   ```

2. Install fontforge

   ```console
   sudo apt-get install fontforge
   ```

   ???+ warning
   Since the PPA for fontforge is no longer maintained, apt might not work for some users.
   The preferred way to install is using the AppImage from: https://fontforge.org/en-US/downloads/

3. Clone the repository or your fork

   ```console
   git clone https://github.com/yashlamba/handwrite
   ```

4. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

5. In the project directory, create the environment and install the project:

   ```console
   uv sync --all-groups
   ```

6. Make sure the tests run:

   ```console
   uv run python -m unittest discover
   ```

7. Install pre-commit hooks before contributing:

   ```console
   uv run pre-commit install
   ```

You are ready to go!

## Windows

1. Install [Potrace](http://potrace.sourceforge.net/#downloading) and make sure it's in your PATH.

2. Install [fontforge](https://fontforge.org/en-US/downloads/) and make sure scripting is enabled.

3. Clone the repository or your fork

   ```console
   git clone https://github.com/yashlamba/handwrite
   ```

4. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

5. In the project directory, create the environment and install the project:

   ```console
   uv sync --all-groups
   ```

6. Make sure the tests run:

   ```console
   uv run python -m unittest discover
   ```

7. Install pre-commit hooks before contributing:

   ```console
   uv run pre-commit install
   ```

You are ready to go!

## Setting Up Docs

1. Install the documentation dependencies:

```bash
uv sync --group docs
```

2. Check the installations by executing this command:

```bash
uv run mkdocs --version
```

    !!! warning ""
        If this doesn't work, try restarting the terminal

3. Use the below command to host the documentation on local server

```bash
uv run mkdocs serve --dev-addr 127.0.0.1:8000
```

{== MkDocs supports live reload so you don't have to run the server again and again. Just save the changes in the docs and you'll see the change immediately. ==}

4. All the documentation is present in the `docs` directory.
