


from app import create_app, db


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db} # Post?


@app.before_first_request
def init_db(*args, **kwargs):
    db.create_all()
    return


if __name__ == '__main__':
    app.run()


