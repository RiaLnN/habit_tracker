from fastapi import FastAPI


def get_app():
    app = FastAPI(title="Habbit Tracker")

    return app

app = get_app()