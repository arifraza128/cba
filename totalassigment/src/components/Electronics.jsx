import { Link, Outlet } from 'react-router-dom';

function Electronics() {
  return (
    <div>
      <h2>Electronics</h2>

      <nav>
        <Link to="/products/electronics/laptops">Laptops</Link>
        <Link to="/products/electronics/mobiles">Mobiles</Link>
      </nav>

      <Outlet />
    </div>
  );
}

export default Electronics;
