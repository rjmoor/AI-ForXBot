from flask import Blueprint, Flask, jsonify, request

'''
Creates the Flask app and registers the blueprints. Defines the API routes.
'''

# Define the main blueprint
main = Blueprint('main', __name__)

# Define the API blueprint
bp = Blueprint('api', __name__)

# Define your routes for the main blueprint
@main.route("/", methods=['GET'])
def main_route():
    """
    Root route for the application.
    """
    return jsonify({'message': 'Welcome to the trading API!'}), 200

# Status endpoint
@bp.route('/status', methods=['GET'])
def status():
    """
    Returns a status message indicating that the API is active.
    """
    return jsonify({'status': 'active'}), 200

# Start trading endpoint
@bp.route('/start', methods=['POST'])
def start():
    """
    Starts trading by calling the start_trading function in the controller.
    """
    return jsonify({'message': 'Trading started'}), 200

# Stop trading endpoint
@bp.route('/stop', methods=['POST'])
def stop():
    """
    Stops trading by calling the stop_trading function in the controller.
    """
    return jsonify({'message': 'Trading stopped'}), 200

# Configure settings endpoint
@bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """
    Retrieves or updates settings based on the request method.
    """
    if request.method == 'GET':
        settings_data = {}  # Replace with actual settings retrieval logic
        return jsonify(settings_data), 200
    elif request.method == 'POST':
        new_settings = request.json
        # Add logic to update settings
        return jsonify({'message': 'Settings updated'}), 200

# Trading performance endpoint
@bp.route('/performance', methods=['GET'])
def performance():
    """
    Retrieves trading performance metrics.
    """
    performance_data = {}  # Replace with actual performance retrieval logic
    return jsonify(performance_data), 200

# Trade history endpoint
@bp.route('/trade-history', methods=['GET'])
def trade_history():
    """
    Retrieves trade history.
    """
    trade_history_data = []  # Replace with actual trade history retrieval logic
    return jsonify(trade_history_data), 200

# Define the create_app function
def create_app():
    """
    Initializes the Flask app and registers the blueprints.
    """
    app = Flask(__name__)
    # Register the blueprints
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(bp, url_prefix='/api')
    
    # Optionally, print the URL rules to verify routing
    for rule in app.url_map.iter_rules():
        print(rule)
    
    return app
