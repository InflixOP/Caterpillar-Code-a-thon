from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/enhance', methods=['POST'])
def enhance_report():
    data = request.json
    report = data.get("report", "")

    # Example enhancement: append a fixed message
    enhanced_report = f"{report} (Enhanced with additional insights)"
    
    return jsonify({"enhanced_report": enhanced_report})

if __name__ == '__main__':
    app.run(port=5001)  # Run on a different port
