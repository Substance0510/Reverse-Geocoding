from app import create_app, api
from app.views import initialize_routes

app = create_app()
initialize_routes(api)

# Use 'adhoc' for self-signed certificates or provide the path to the certificate and key files
# ssl_context = 'adhoc'
ssl_context = ('ssl/cert.pem', 'ssl/key.pem')

if __name__ == '__main__':
    app.run(
        debug=True,  # Set to False in production
        ssl_context=ssl_context,
    )
