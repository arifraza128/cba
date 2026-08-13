import { useRef, useState } from 'react';

function UncontrolledName() {
  const nameInput = useRef(null);
  const [submittedName, setSubmittedName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmittedName(nameInput.current.value);
  };

  return (
    <div>
      <h2>Uncontrolled Component</h2>

      <form onSubmit={handleSubmit}>
        <input type="text" ref={nameInput} placeholder="Enter name" />
        <button type="submit">Submit</button>
      </form>

      <p>Name: {submittedName}</p>
    </div>
  );
}

export default UncontrolledName;
