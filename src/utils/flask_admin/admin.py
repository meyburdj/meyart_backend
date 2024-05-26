# # src/admin.py
# import boto3
# from flask import request, redirect, url_for
# from flask_admin import Admin, BaseView, expose
# from flask_admin.contrib.sqla import ModelView
# from werkzeug.utils import secure_filename
# from src import db
# from src.api.artworks.models import Artwork

# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
# )

# def upload_file_to_s3(file, bucket_name, acl="public-read"):
#     try:
#         s3.upload_fileobj(
#             file,
#             bucket_name,
#             file.filename,
#             ExtraArgs={
#                 "ACL": acl,
#                 "ContentType": file.content_type
#             }
#         )
#     except Exception as e:
#         print("Something Happened: ", e)
#         return e

#     return f"{app.config['S3_LOCATION']}{file.filename}"

# class ArtworkAdmin(ModelView):
#     form_excluded_columns = ['url']

#     def on_model_change(self, form, model, is_created):
#         if 'file' in request.files:
#             file = request.files['file']
#             if file:
#                 filename = secure_filename(file.filename)
#                 file_url = upload_file_to_s3(file, app.config["S3_BUCKET"])
#                 model.url = file_url

# class FileUploadView(BaseView):
#     @expose('/', methods=('GET', 'POST'))
#     def index(self):
#         if request.method == 'POST':
#             file = request.files['file']
#             if file:
#                 filename = secure_filename(file.filename)
#                 file_url = upload_file_to_s3(file, app.config["S3_BUCKET"])
#                 # Save the file URL to the database if necessary
#                 return redirect(url_for('fileuploadview.index'))

#         return self.render('admin/file_upload.html')

# # Create an instance of the admin interface
# admin = Admin(app, name='Meyart Gallery Admin', template_mode='bootstrap3')

# # Add administrative views here
# admin.add_view(ArtworkAdmin(Artwork, db.session))
# admin.add_view(FileUploadView(name='File Upload'))


# utils/flask_admin/admin.py
import os
from flask import request, redirect, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
from src import db
from src.api.artworks.models import Artwork
from src.api.artists.models import Artist

class ArtworkAdmin(ModelView):
    form_excluded_columns = ['url']

    def on_model_change(self, form, model, is_created):
        if 'file' in request.files:
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                # For now, just use the file name; S3 URL will be added later
                model.url = f"/static/uploads/{filename}"

class FileUploadView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                # Save the file locally for now; S3 integration will come later
                file.save(os.path.join('static/uploads', filename))
                return redirect(url_for('fileuploadview.index'))

        return self.render('admin/file_upload.html')

def init_admin(app):
    admin = Admin(app, name='Meyart Gallery Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(Artist, db.session))
    admin.add_view(ArtworkAdmin(Artwork, db.session))
    admin.add_view(FileUploadView(name='File Upload'))
