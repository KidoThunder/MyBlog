import logging
# from logging.handlers import SMTPHandler
import os
from logging.handlers import RotatingFileHandler

from flask import render_template

from blog import app, db


@app.errorhandler(404)
def not_found_page(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def interval_error(error):
    db.session.rollback()
    if not app.debug:
        # if app.config["MAIL_SERVER"]:
        #     auth = None
        #     if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
        #         auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        #     secure = None
        #     if app.config["MAIL_USE_TLS"]:
        #         secure = ()
        #     mail_handler = SMTPHandler(
        #         mailhost=(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"]),
        #         fromaddr="no-reply@" + app.config["MAIL_SERVER"],
        #         toaddrs=app.config["ADMINS"],
        #         subject="Myblog Failure",
        #         credentials=auth,
        #         secure=secure)
        #     mail_handler.setLevel(logging.ERROR)
        #     app.logger.addHandler(mail_handler)
        if not os.path.exists("logs"):
            os.mkdir("logs")

        file_handler = RotatingFileHandler(
            "logs/myblog.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
            ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("MyBlog startup")
    return render_template("500.html"), 500
