import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

model = joblib.load('finalmodel1.joblib')
label_encoders = joblib.load('label_encoders.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from the form
    data = request.form.to_dict()

    features = np.array([
        float(data['leftFrontPressure']),
        float(data['rightFrontPressure']),
        label_encoders['Left Front Condition'].transform([data['leftFrontCondition']])[0],
        label_encoders['Right Front Condition'].transform([data['rightFrontCondition']])[0],
        float(data['leftRearPressure']),
        float(data['rightRearPressure']),
        label_encoders['Left Rear Condition'].transform([data['leftRearCondition']])[0],
        label_encoders['Right Rear Condition'].transform([data['rightRearCondition']])[0],
        label_encoders['Battery Water Level'].transform([data['batteryWaterLevel']])[0],
        label_encoders['Battery Condition'].transform([data['batteryCondition']])[0],
        label_encoders['Battery Leak'].transform([data['batteryLeak']])[0],
        float(data['batteryReplacementDate']),
        label_encoders['Rust/Dent/ Damage Exterior'].transform([data['rustDentDamageExterior']])[0],
        label_encoders['Oil Leak in Suspension'].transform([data['oilLeakSuspension']])[0],
        label_encoders['Brake Fluid Level'].transform([data['brakeFluidLevel']])[0],
        label_encoders['Brake Condition Front'].transform([data['brakeConditionFront']])[0],
        label_encoders['Brake Condition Rear'].transform([data['brakeConditionRear']])[0],
        label_encoders['Emergency Brake'].transform([data['emergencyBrake']])[0],
        label_encoders['Rust/Dent/Damage Engine'].transform([data['rustDentDamageEngine']])[0],
        label_encoders['Engine Oil Condition'].transform([data['engineOilCondition']])[0],
        label_encoders['Engine Oil Color'].transform([data['engineOilColor']])[0],
        label_encoders['Brake Fluid Condition'].transform([data['brakeFluidCondition']])[0],
        label_encoders['Brake Fluid Color'].transform([data['brakeFluidColor']])[0],
        label_encoders['Oil Leak in Engine'].transform([data['oilLeakEngine']])[0]
    ]).reshape(1, -1)

    prediction = model.predict(features)

    return jsonify({'costing': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
