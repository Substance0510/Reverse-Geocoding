from app import create_app, api
from app.views import initialize_routes

app = create_app()
initialize_routes(api)

if __name__ == '__main__':
    app.run(debug=True)
