import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb+srv://zakaur:GwSfTDvrIPPhR2eE@jobtest.n2s3tgo.mongodb.net/user_details?retryWrites=true&w=majority'