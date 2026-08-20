import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  const increase = () => {
    setCount((prev) => prev + 1);
  };

  const decrease = () => {
    setCount((prev) => (prev > 0 ? prev - 1 : 0));
  };

  return (
    <div>
      <h2>Counter</h2>

      <div className="counter-row">
        <button onClick={decrease}>-</button>
        <span className="count-value">{count}</span>
        <button onClick={increase}>+</button>
      </div>

      {count === 10 && <p className="success-text">🎉 Count reached 10!</p>}
    </div>
  );
}

export default Counter;
