import json
import googlemaps
from flask import Flask, request, jsonify
from flask_cors import CORS
from pprint import pprint
from map import get_input_prompt_for_location
from bot_tools import Conversation

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

conv_hist = Conversation()
conv_hist.load()



@app.route('/send-message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')

    if user_message:
        conv_hist.appendu(user_message)
        bot_response = conv_hist.complete()
        conv_hist.dump()

        return jsonify({'response': bot_response})
    else:
        return jsonify({'response': 'Invalid request'})

@app.route('/conversation-history', methods=['GET'])
def get_conversation_history():
    return jsonify(conv_hist.messages_for_user)

@app.route('/location-clicked', methods=['POST'])
def handle_location_clicked():
    data = request.form
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Obtain location information using latitude and longitude coordinates
    message_s, message_u = get_input_prompt_for_location(float(latitude), float(longitude))
    print(message_s)
    print(message_u)
    # Update the conversation history with the location message
    conv_hist.append_location_description_request(message_s, message_u)
    response_message = conv_hist.complete()
    conv_hist.dump()
    print(response_message)


    return jsonify({'response': response_message})

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
