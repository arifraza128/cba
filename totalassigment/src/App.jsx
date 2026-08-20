import { BrowserRouter, Routes, Route, NavLink, Outlet } from 'react-router-dom';
import Counter from './components/Counter';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';
import FileUpload from './components/FileUpload';
import ControlledName from './components/ControlledName';
import UncontrolledName from './components/UncontrolledName';
import Products from './components/Products';
import Electronics from './components/Electronics';
import Laptops from './components/Laptops';
import Mobiles from './components/Mobiles';
import Clothing from './components/Clothing';
import ProductCards from './components/ProductCards';
import NavbarDemo from './components/Navbar';
import Posts from './components/Posts';
import './components/ProductCards.css';

function Admin() {
  return (
    <div className="admin-layout">
      <aside className="sidebar">
        <h2>Admin</h2>

        <NavLink to="/admin" end>
          Dashboard
        </NavLink>
        <NavLink to="/admin/users">Users</NavLink>
        <NavLink to="/admin/products">Products</NavLink>
        <NavLink to="/admin/orders">Orders</NavLink>
        <NavLink to="/admin/settings">Settings</NavLink>
      </aside>

      <main className="admin-content">
        <Outlet />
      </main>
    </div>
  );
}

function Dashboard() {
  return <h1>Admin Dashboard</h1>;
}

function Users() {
  return <h1>Users Management</h1>;
}

function ManageProducts() {
  return <h1>Products Management</h1>;
}

function Orders() {
  return <h1>Orders Management</h1>;
}

function Settings() {
  return <h1>Admin Settings</h1>;
}

function App() {
  return (
    <BrowserRouter>
      <div className="assignment-app">
        <h1>React Assignment Collection</h1>

        <div className="section">
          <Counter />
        </div>

        <div className="section">
          <LoginForm />
        </div>

        <div className="section">
          <RegistrationForm />
        </div>

        <div className="section">
          <FileUpload />
        </div>

        <div className="section">
          <ControlledName />
        </div>

        <div className="section">
          <UncontrolledName />
        </div>

        <div className="section">
          <h2>Nested Routes – Product Application</h2>
          <Routes>
            <Route path="/products" element={<Products />}>
              <Route path="electronics" element={<Electronics />}>
                <Route path="laptops" element={<Laptops />} />
                <Route path="mobiles" element={<Mobiles />} />
              </Route>
              <Route path="clothing" element={<Clothing />} />
            </Route>
          </Routes>
        </div>

        <div className="section">
          <h2>Nested Routes – Admin Dashboard</h2>
          <Routes>
            <Route path="/admin" element={<Admin />}>
              <Route index element={<Dashboard />} />
              <Route path="users" element={<Users />} />
              <Route path="products" element={<ManageProducts />} />
              <Route path="orders" element={<Orders />} />
              <Route path="settings" element={<Settings />} />
            </Route>
          </Routes>
        </div>

        <div className="section">
          <h2>CSS Styling – Product Cards</h2>
          <ProductCards />
        </div>

        <div className="section">
          <h2>Posts from API</h2>
          <Posts />
        </div>

        <div className="section">
          <h2>CSS Styling – Responsive Navigation Bar</h2>
          <div className="navbar-demo">
            <NavbarDemo />
          </div>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
