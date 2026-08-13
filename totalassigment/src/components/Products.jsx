import { Link, Outlet } from 'react-router-dom';

function Products() {
  return (
    <div className="route-demo">
      <h1>Products</h1>

      <nav>
        <Link to="/products/electronics">Electronics</Link>
        <Link to="/products/clothing">Clothing</Link>
      </nav>

      <Outlet />
    </div>
  );
}

export default Products;
