import { useState } from 'react';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submittedEmail, setSubmittedEmail] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    setSubmittedEmail(email);
    setSuccess(Boolean(email && password));
  };

  return (
    <div>
      <h2>Login Form</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Login</button>
      </form>

      {submittedEmail && <p>Entered Email: {submittedEmail}</p>}

      {success && <p className="success-text">Login successful</p>}
    </div>
  );
}

export default LoginForm;
