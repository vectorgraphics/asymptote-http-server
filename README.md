
# Asymptote HTTP Server

A small HTTP server that exposes the Asymptote
[command-line interface](https://asymptote.sourceforge.io/doc/Command_002dLine-Interface.html)
as a simple API: send Asymptote source code as the request body and receive the
compiled output. It is written in [Python 3](https://www.python.org/) with
[Tornado](https://www.tornadoweb.org/).

## Public endpoint

The service is fronted by an `nginx` reverse proxy that terminates TLS and
forwards to `127.0.0.1:10007`:

- **HTTPS (preferred):** `https://asymptote.ualberta.ca/cli`
- Plain HTTP on port `10007` (`http://asymptote.ualberta.ca:10007`) is also
  available for now, but the direct port is expected to be discontinued in the
  future. Use the HTTPS endpoint.

The relevant `nginx` location is an exact match on `/cli`:

```nginx
location = /cli {
  proxy_pass http://127.0.0.1:10007/;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  client_max_body_size 20m;
  proxy_read_timeout 300s;
  proxy_send_timeout 300s;
}
```

## Usage

Send your `.asy` source as the **POST** body. Choose the output format with the
`f` (or `outformat`) query argument; other `asy` command-line options are passed
as additional query arguments.

```bash
# SVG output
curl --data-binary 'import venn;' 'https://asymptote.ualberta.ca/cli?f=svg' | display -

# PDF output
curl --data-binary 'import venn;' 'https://asymptote.ualberta.ca/cli?f=pdf' -o venn.pdf

# HTML output
curl --data-binary @/usr/local/share/doc/asymptote/examples/Klein.asy 'https://asymptote.ualberta.ca/cli' -o Klein.html

# V3D output
curl --data-binary 'import teapot;' 'https://asymptote.ualberta.ca/cli?f=v3d' -o teapot.v3d

# PDF output with embedded V3D content and rendered bitmap at 2 pixels per bp
curl --data-binary 'import teapot;' 'https://asymptote.ualberta.ca/cli?f=pdf&v3d' -o teapot.pdf

# PDF output with rendered bitmap at 2 pixels per bp
curl --data-binary 'import teapot;' 'https://asymptote.ualberta.ca/cli?f=pdf' -o teapot.pdf

# PDF output with rendered bitmap at 4 pixels per bp
curl --data-binary 'import teapot;' 'https://asymptote.ualberta.ca/cli?f=pdf&render=4' -o teapot.pdf
```

A `GET` to the endpoint returns the server's `asy -version` string (a handy
health check).

## Options

| Query argument      | Meaning                                                                     |
|---------------------|-----------------------------------------------------------------------------|
| `f` / `outformat`   | Output format (`svg`, `pdf`, `html`, `v3d`, `eps`, ...). Default `html`.    |
| any other `asy` opt | Passed through as an `asy` command-line option (e.g. `render=4`).           |

Each request runs `asy` in a fresh temporary directory, which is removed when
the request completes.

## Responses

| Status | Meaning                                                        |
|--------|----------------------------------------------------------------|
| `200`  | Success -- the compiled output is the response body.            |
| `204`  | `asy` succeeded but produced no output file.                   |
| `408`  | The compile exceeded the server timeout.                       |
| `415`  | `asy` failed; the body is JSON `{"msg": ..., "reason": ...}`.  |

## Running locally

```bash
python3 server.py --port 10007 --timeout 300
```

- `--port` (default `10007`): port to listen on.
- `--timeout` (default `300`): per-request `asy` timeout, in seconds.

When started as root, the server drops privileges to the user and group named by
the `ASYMPTOTE_USER` / `ASYMPTOTE_GROUP` environment variables (default
`asymptote`).

## Installation (systemd)

```bash
make install                 # installs the .py files to /usr/local/share/asyserver
                             # and asyserver.service to /lib/systemd/system
sudo systemctl enable --now asyserver
```

The service runs `server.py --port 10007 --timeout 300` as the `asymptote`
user. In production the public HTTPS endpoint (`/cli`) is served by the `nginx`
location shown above, which forwards requests to `127.0.0.1:10007`.

