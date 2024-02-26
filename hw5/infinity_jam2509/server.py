import json
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)
current_id = 4

clients = [
"Shake Shack",
"Toast",
"Computer Science Department", "Teacher's College",
"Starbucks",
"Subsconsious",
"Flat Top",
"Joe's Coffee",
"Max Caffe",
"Nussbaum & Wu",
"Taco Bell",
]
sales = [
    {
        "id": 1,
        "salesperson": "James D. Halpert",
        "client": "Shake Shack",
        "reams": 100
    },
    {
        "id":2,
        "salesperson": "Stanley Hudson",
        "client": "Toast",
        "reams": 400
    },
    {
        "id":3,
        "salesperson": "Michael G. Scott",
        "client": "Computer Science Department",
        "reams": 1000
    },
]


# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/infinity')
def logs():
    return render_template('log_sales.html',clients=clients, sales=sales)
@app.route('/save_sale', methods=['POST'])
def save_sale():
    global current_id
    global sales
    global clients
    
    # Extract the data sent from the client
    sales_data = request.get_json()
    sales.append(sales_data)
    sales_data["id"] = current_id
    current_id += 1

    sales_client = sales_data["client"]
    if sales_client not in clients:
        clients.append(sales_client)

    # Return a response to the client
    return jsonify(sales = sales, clients = clients), 200

@app.route('/delete_sale/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    global sales
    sales = [sale for sale in sales if sale['id'] != sale_id]

    # Return the updated sales list
    return jsonify(sales=sales), 200

if __name__ == '__main__':
    app.run(debug=True)
