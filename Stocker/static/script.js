// Utility function for fetch requests with enhanced error handling
async function sendRequest(endpoint, method, bodyData) {
  try {
    const response = await fetch(endpoint, {
      method: method,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(bodyData),
    });

    const data = await response.json();

    // Check HTTP status and handle errors more precisely
    if (!response.ok) {
      throw new Error(data.message || 'An error occurred on the server.');
    }

    return data; // Return data if successful
  } catch (error) {
    console.error(`Error during ${method.toUpperCase()} request to ${endpoint}:`, error);
    alert(error.message || 'Network error. Please try again.');
    return null;
  }
}

// Reusable function to disable/enable buttons during requests
function setButtonState(isLoading, buttonId) {
  const button = document.getElementById(buttonId);
  button.disabled = isLoading;
  button.textContent = isLoading ? 'Processing...' : button.dataset.originalText;
}

// Register function with enhanced UI feedback
async function register() {
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!username || !password) {
    alert('Username and password are required!');
    return;
  }

  setButtonState(true, 'register-btn'); // Disable button during request

  const data = await sendRequest('/register', 'POST', { username, password });
  
  if (data) alert(data.message);
  
  setButtonState(false, 'register-btn'); // Re-enable button
}

// Login function with enhanced security handling
async function login() {
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!username || !password) {
    alert('Username and password are required!');
    return;
  }

  setButtonState(true, 'login-btn'); // Disable login button temporarily

  const data = await sendRequest('/login', 'POST', { username, password });

  if (data && data.user_id) {
    alert(data.message);
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('trade-section').style.display = 'block';
    document.getElementById('user-name').textContent = username;
    sessionStorage.setItem('token', data.token);  // Use JWT for security
  } else {
    alert('Invalid credentials');
  }
  
  setButtonState(false, 'login-btn'); // Re-enable login button
}

// Trade function with improved validation
async function trade() {
  const token = sessionStorage.getItem('token'); // Use token instead of user_id
  const stock_symbol = document.getElementById('stock-symbol').value.trim().toUpperCase();
  const quantity = parseInt(document.getElementById('quantity').value.trim(), 10);
  const transaction_type = document.getElementById('transaction-type').value;
  const price = parseFloat(document.getElementById('price').value.trim());

  // Validate inputs
  if (!stock_symbol || isNaN(quantity) || isNaN(price) || quantity <= 0 || price <= 0) {
    alert('Please enter valid stock symbol, quantity, and price!');
    return;
  }

  const data = await sendRequest('/trade', 'POST', {
    token, // Pass token for user verification
    stock_symbol,
    quantity,
    transaction_type,
    price,
  });

  if (data) alert(data.message);
}
