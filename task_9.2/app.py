from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0]['rates']
#print(rates)
currency = []
for element in rates:
    currency.append(element['currency'])
title_line = []
for element in rates[0]:
    title_line.append(element)

with open('kursy_walut.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=title_line, delimiter=';')
    writer.writeheader()
    writer.writerows(rates)

@app.route("/kalkulator/", methods=["GET", "POST"])
def kalkulatorek():
    if request.method == "POST":
        data = request.form
        currency_from_form = data.get('currency')
        amount = int(data.get('amount'))
        for element in rates:
            if element['currency'] == currency_from_form:
                code = element['code']
                bid = float(element['bid'])
                ask = float(element['ask'])
                cost = ask * amount
                return render_template("kalkulator.html", currency_cal=currency, cost=cost, code=code, bid=bid, ask=ask, currency_from_form=currency_from_form, amount=amount)
    empty = '___'
    return render_template("kalkulator.html", currency_cal=currency, cost=empty, code=empty, bid=empty, ask=empty, currency_from_form=empty, amount=empty)
