import os
from flask import Flask

app = Flask(__name__)

# Disable debug mode for production
app.config['DEBUG'] = False

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
