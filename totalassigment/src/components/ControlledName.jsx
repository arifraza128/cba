import { useState } from 'react';

function ControlledName() {
  const [name, setName] = useState('');
  const [submittedName, setSubmittedName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmittedName(name);
  };

  return (
    <div>
      <h2>Controlled Component</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter name"
        />

        <button type="submit">Submit</button>
      </form>

      <p>Name: {submittedName}</p>
    </div>
  );
}

export default ControlledName;
