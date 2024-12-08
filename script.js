document.getElementById('calculateButton').addEventListener('click', async function () {
  const form = document.getElementById('menuForm');
  const formData = new FormData(form);

  try {
      const response = await fetch('http://localhost:8000/calculate_bill', {
          method: 'POST',
          body: new URLSearchParams(formData),
      });

      if (response.ok) {
          const data = await response.json();
          displayBill(data);
      } else {
          alert('Failed to calculate the bill. Please try again.');
      }
  } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please check the console for details.');
  }
});

function displayBill(data) {
  const billDetails = document.getElementById('billDetails');
  const billItems = document.getElementById('billItems');
  const totalAmount = document.getElementById('totalAmount');

  billItems.innerHTML = '';
  data.details.forEach(detail => {
      const li = document.createElement('li');
      li.textContent = detail;
      billItems.appendChild(li);
  });

  totalAmount.textContent = data.total;
  billDetails.classList.remove('hidden');
}
