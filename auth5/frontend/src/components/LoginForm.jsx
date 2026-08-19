import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setMessage('Please enter both email and password.');
      return;
    }
    setIsLoading(true);
    setMessage('');
    try {
      const response = await api.post('/', {
        email,
        password,
      });
      localStorage.setItem('token', response.data.token);
      navigate('/profile');
    } catch (error) {
      setMessage(error.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="glass-card login-card">
        <div className="card-header">
          <div className="logo-glow"></div>
          <h2>Secure Portal</h2>
          <p className="subtitle">Sign in to access your dashboard</p>
        </div>
        
        <form onSubmit={handleLogin} className="login-form">
          <div className="input-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? (
              <span className="spinner"></span>
            ) : (
              'Authenticate'
            )}
          </button>
          
          {message && (
            <div className={`feedback-message ${message.includes('success') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}
        </form>

        <div className="credentials-hint">
          <p className="hint-title">Demo Access Credentials</p>
          <div className="hint-row">
            <span>Email:</span> <code>hari@gmail.com</code>
          </div>
          <div className="hint-row">
            <span>Password:</span> <code>hari123</code>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginForm;
