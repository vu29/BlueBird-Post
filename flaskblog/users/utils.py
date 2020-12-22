import os
from PIL import Image
from flaskblog import mail
from flask import current_app
from flask import url_for
from flask_mail import Message
from flask_login import current_user


def save_picture(form_picture):
    prev_pic_filename = current_user.user_image
    if prev_pic_filename != "default.jpg":
        prev_pic_path = os.path.join(current_app.root_path,"static/dp",prev_pic_filename)
        os.remove(prev_pic_path)
    _,pic_ext = os.path.splitext(form_picture.filename)
    pic_filename = str(current_user.id) + pic_ext
    file_path = os.path.join(current_app.root_path,"static/dp",pic_filename)
    form_picture = Image.open(form_picture)
    form_picture.thumbnail((300,300),Image.ANTIALIAS)
    form_picture.save(file_path)
    return pic_filename

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message("Reset Password",
        sender = "BlueBird Post<vibhu.upamanyu@gmail.com>",
        recipients=[user.email])
    message.body = f''' To reset your password visit the link:
{url_for('users.reset_password', token = token, _external=True )}

If you did not make this requet please ignore.
'''
    mail.send(message)