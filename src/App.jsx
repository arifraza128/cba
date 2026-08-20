import { useRef, useState } from 'react';

function ControlledForm() {
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Hello ${name}`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Controlled Form</h2>

      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
      />

      <p>Your name is: {name}</p>

      <button type="submit">Submit</button>
    </form>
  );
}

function UnControlledForm() {
  const nameRef = useRef('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Hello ${nameRef.current?.value}`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Uncontrolled Form</h2>

      <input type="text" ref={nameRef} placeholder="Enter your name" />

      <p>Your name is: {nameRef.current?.value}</p>

      <button type="submit">Submit</button>
    </form>
  );
}

export default function App() {
  return (
    <>
      <ControlledForm />
      <UnControlledForm />
    </>
  );
}
