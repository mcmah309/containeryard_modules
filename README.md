Module repository for https://github.com/mcmah309/containeryard 

Downloads must fail the build on HTTP or transport errors. Use `curl --fail`
and download to a file before running an installer, extracting an archive, or
importing a key. Chain each step with `&&`; piping a download into another
command can hide the downloader's failure under Docker's default shell.
Check the installed executable with `--version` when available.

Run `python3 -m unittest discover -s tests -v` with `yard` on PATH to check
all module downloads and simulate failures in rendered Containerfiles,
including pinned and default installer versions. These checks need no network
or Docker daemon.
