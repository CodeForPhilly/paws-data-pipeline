# Troubleshooting

This section contains troubleshooting for the PAWS data pipeline project.

## Windows

### Port 3000 not available

`ERROR: for paws-compose-client Cannot start service client: Ports are not available: listen tcp 0.0.0.0:3000: bind: An attempt was made to access a socket in a way forbidden by its access permissions.`

This error can be caused by Hyper-V reserving TCP port 3000 (Node/Express default port), which prevents Docker from exposing it outside the container.

You can verify this by running `netsh interface ipv4 show excludedportrange protocol=tcp` You'll see 3000 within a reserved range.\
There are three solutions:

* Disable Hyper-V and run Docker via WSL2 (best solution)\
  See [Disable Hyper-V](https://docs.microsoft.com/en-us/troubleshoot/windows-client/application-management/virtualization-apps-not-work-with-hyper-v) and [Run Docker on WSL2](https://docs.docker.com/docker-for-windows/wsl/)
* Disable Hyper-V, reserve the port for Docker, re-enable Hyper-V\
  See this [Docker issue](https://github.com/docker/for-win/issues/3171#issuecomment-459205576)
* Expose the client on a non-reserved port\
  Edit the client section of `docker-compose.yml` and change 3000:3000 to 8000:3000 (or other available port)

### The RPC server is not available

When trying to start, newer versions of Docker may give an error message that says, "The RPC server is not available."

Open Docker, go to Settings (the gear button at the top), General, and make sure the checkbox next to "Use the WSL 2 based engine" is unchecked. Apply and restart.

### startServer.sh: not found

The issue is that Git has changed your line endings from Unix-style LF to Windows-style CRLF, so your files aren't being identified.

In Command Prompt, navigate to your base PAWS directory and enter the following two commands:

`git config --global core.eol lf`

`git config --global core.autocrlf input`

### Docker API unavailable

`[HPM] Error occurred while trying to proxy request /api/user/login from localhost:3000 to http://server:5000 (ENOTFOUND) (https://nodejs.org/api/errors.html#errors_common_system_errors)`

* In `C:\Windows\System32\drivers\etc\hosts`, add `127.0.0.1 server`
