from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    # Extract input values from the request (data)
    current_age = int(data.get('currentAge'))
    current_corpus = int(data.get('currentCorpus'))
    current_income = int(data.get('currentIncome'))
    annual_increase = float(data.get('annualIncrease'))
    investment_proportion = float(data.get('investmentProportion'))
    investment_return = float(data.get('investmentReturn'))
    target_corpus = int(data.get('targetCorpus')) # 1 crore = 10,000,000

    year = 0
    fund_start = current_corpus

    while fund_start < target_corpus:
        year += 1
        age = current_age + year
        annual_income = current_income * (1 + annual_increase)**year  # Updated for exponential growth
        amount_invested = annual_income * investment_proportion
        investment_return_amount = fund_start * investment_return
        fund_end = fund_start + amount_invested + investment_return_amount
        fund_start = fund_end # update starting fund

    result = {
        "ageAtTarget": age
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # For local testing
