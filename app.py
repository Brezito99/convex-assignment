import os
import importlib
from flask import Flask, send_from_directory, send_file, Response


def create_app() -> Flask:
    """Create a configured Flash app instance."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(
        "config.config.Config"
    )
    app.secret_key = os.getenv('SECRET_KEY')

    route_files = []
    route_names = []

    for root, _, files in os.walk('./routes'):
        route_files = [os.path.join(root, route_filename) for route_filename in files]
        route_names = [route_filename.rpartition('.py')[0] + '_blueprint' for route_filename in files]
        break

    for module_path, blueprint_name in zip(route_files, route_names):

        if blueprint_name.startswith('_') or blueprint_name.startswith('.'):
            continue

        spec = importlib.util.spec_from_file_location(blueprint_name, module_path)

        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)

        # Get the blueprint from the module
        blueprint = getattr(imported_module, blueprint_name)

        app.register_blueprint(blueprint)

    @app.route('/assets/<path:path>')
    def send_js(path) -> Response:
        """Send assets (JS, CSS, etc.)"""
        return send_from_directory('static/assets', path)

    @app.route('/')
    def send_index() -> Response:
        """Send static HTML page for the front-end."""
        return send_file('static/index.html')

    return app


if __name__ == '__main__':
    create_app().run()
