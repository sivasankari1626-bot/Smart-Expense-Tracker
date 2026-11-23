from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# SQLite Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Expense Database Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' or 'expense'
    date = db.Column(db.String(20), default=datetime.utcnow().strftime('%Y-%m-%d'))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': self.amount,
            'category': self.category,
            'type': self.type,
            'date': self.date
        }

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

# Get all transaction records & calculated summary
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = Expense.query.order_by(Expense.id.desc()).all()
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    return jsonify({
        'transactions': [t.to_dict() for t in transactions],
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    })

# Add new transaction
@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    new_item = Expense(
        title=data['title'],
        amount=float(data['amount']),
        category=data['category'],
        type=data['type']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Added successfully!', 'item': new_item.to_dict()}), 201

# Delete a transaction
@app.route('/api/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    item = Expense.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)