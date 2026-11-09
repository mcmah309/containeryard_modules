Module repository for https://github.com/mcmah309/containeryard 

Downloads must fail the build on HTTP or transport errors. Use `curl --fail`
and download to a file before running an installer, extracting an archive, or
importing a key. Chain each step with `&&`; piping a download into another
command can hide the downloader's failure under Docker's default shell.
Check the installed executable with `--version` when available.

Install test dependencies with `python3 -m pip install -r tests/requirements.txt`,
then run `python3 -m unittest discover -s tests -v` with `yard` on PATH.
The tests automatically discover download recipes, supply synthetic required
arguments, and test both default and explicitly supplied version arguments.
No recipe list or per-recipe overrides are needed. The checks simulate download
failures in rendered Containerfiles without a network or Docker daemon.
