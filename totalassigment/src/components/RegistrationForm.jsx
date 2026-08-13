import { useState } from 'react';

function RegistrationForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [age, setAge] = useState('');

  return (
    <div>
      <h2>Registration Form</h2>

      <form>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

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

        <input
          type="number"
          placeholder="Age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />

        {age && Number(age) < 18 && (
          <p className="error-text">Age must be 18 or above.</p>
        )}
      </form>

      <div className="current-values">
        <h3>Current Form Values</h3>
        <p>Name: {name}</p>
        <p>Email: {email}</p>
        <p>Password: {password}</p>
        <p>Age: {age}</p>
      </div>
    </div>
  );
}

export default RegistrationForm;
