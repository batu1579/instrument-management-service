from uvicorn import run

from app.util import env

if env.USE_HTTPS_ONLY and (env.KEYFILE is None or env.CERTFILE is None):
    raise ValueError(
        "KEYFILE and CERTFILE must be supplied When USE_HTTPS_ONLY is set to True."
    )

if __name__ == "__main__":
    run(
        app="app.main:app",
        host=env.HOST,
        port=env.PORT,
        ssl_keyfile=env.KEYFILE,
        ssl_certfile=env.CERTFILE,
    )
