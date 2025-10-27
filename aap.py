from flask import Flask,render_template,request,jsonify
import requests

RASA_API_URL=''

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('Homepage.html')
@app.route('/about')
def about():
    return render_template('About page.html')
@app.route('/lets_chat')
def lets_chat():
    return render_template('chat_page.html')

@app.route('/webhook',methods=['POST'])
def webhook():
    user_message= request.json.get('message')
    if not user_message:
        return jsonify({'response':'No message received '}), 400
    
    try:
        rasa_response = request.post(RASA_API_URL,json={'message':user_message})
        rasa_response.raise_for_status()
        rasa_response_json=rasa_response.json()
        print(f"Rasa response JSON:{rasa_response_json}")
        if rasa_response_json and 'text' in rasa_response_json[0]:
            bot_response = rasa_response_json[0]['text']
        else:
            bot_response="sorry, I didn't understand that."
    except  Exception as e:
        print(f"Error communicating with Rasa: {e}")
        bot_response="sorry,there was an error connecting to the chatbot."
    return jsonify({'response':bot_response})

if __name__ == '__main__':
    app.run(debug=True)                