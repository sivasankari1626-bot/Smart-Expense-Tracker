document.addEventListener('DOMContentLoaded', fetchTransactions);

const form = document.getElementById('transaction-form');

// Load data from Python Backend
async function fetchTransactions() {
    const res = await fetch('/api/transactions');
    const data = await res.json();

    // Update Top Cards
    document.getElementById('total-income').innerText = `₹${data.total_income}`;
    document.getElementById('total-expense').innerText = `₹${data.total_expense}`;
    document.getElementById('net-balance').innerText = `₹${data.balance}`;

    // Update Bottom Table Summary (Income, Expense & Calculated Net Balance)
    const balanceColor = data.balance >= 0 ? 'text-primary' : 'text-danger';
    
    document.getElementById('summary-total').innerHTML = 
        `<span class="text-success">+₹${data.total_income}</span> | ` +
        `<span class="text-danger">-₹${data.total_expense}</span> | ` +
        `Net: <span class="${balanceColor}">₹${data.balance}</span>`;

    const list = document.getElementById('transaction-list');
    list.innerHTML = '';

    data.transactions.forEach(t => {
        const row = document.createElement('tr');
        const badgeClass = t.type === 'income' ? 'text-success fw-bold' : 'text-danger fw-bold';
        const sign = t.type === 'income' ? '+' : '-';

        row.innerHTML = `
            <td>${t.title} <br><small class="text-muted">${t.date}</small></td>
            <td><span class="badge bg-secondary">${t.category}</span></td>
            <td class="${badgeClass}">${sign} ₹${t.amount}</td>
            <td><button class="btn btn-sm btn-outline-danger" onclick="deleteTransaction(${t.id})">Delete</button></td>
        `;
        list.appendChild(row);
    });
}

// Add new transaction via API
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        title: document.getElementById('title').value,
        amount: document.getElementById('amount').value,
        type: document.getElementById('type').value,
        category: document.getElementById('category').value
    };

    await fetch('/api/transactions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    form.reset();
    fetchTransactions();
});

// Delete transaction via API
async function deleteTransaction(id) {
    if (confirm('Are you sure you want to delete this record?')) {
        await fetch(`/api/transactions/${id}`, { method: 'DELETE' });
        fetchTransactions();
    }
}