from flask import Flask, request, jsonify
from rate_limiter import RateLimiter

app = Flask(__name__)

rate_limiter = RateLimiter(limit_per_second=5)

@app.route('/', methods=['GET'])
def index():
    return {"status": "Up and Healthy!"}, 200

@app.route('/api/check-rate-limit-one', methods=['GET'])
def check_rate_limit():
    """
    Check if the rate limit is exceeded for the given user ID.
    """
    ip = request.headers.get('X-Forwarded-For', request.remote_addr) 
    
    #Instead of IP address, we can use the user ID if an auth system is implemented

    if rate_limiter.is_allowed(ip):
        return jsonify({"status": "Yep, allowed."}), 200
    else:
        return jsonify({"status": "Nope, Rate limit exceeded"}), 429
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
