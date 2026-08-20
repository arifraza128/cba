import { useState } from 'react';

function LoginForm() {
  const [username, setUserName] = useState('');
  const [passwd, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    const credentials = btoa(`${username}:${passwd}`);

    try {
      const response = await fetch('http://localhost:5000/api/hello', {
        method: 'GET',
        headers: {
          Authorization: `Basic ${credentials}`,
        },
      });

      if (response.ok) {
        const data = await response.text();
        alert(data);
      } else {
        alert('Invalid Username or Password');
      }
    } catch (error) {
      console.error(error);
      alert('Server error');
    }
  };

  return (
    <div>
      <h2>Basic Authentication</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>UserName:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUserName(e.target.value)}
          />
        </div>
        <br />
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={passwd}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginForm;