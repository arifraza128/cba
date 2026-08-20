import { Link, Outlet } from "react-router-dom";


function Dashboard() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside
        style={{
          width: "200px",
          padding: "20px",
          borderRight: "1px solid #ccc",
        }}
      >
        <h2>Dashboard</h2>


        <nav>
          <p>
            <Link to="/dashboard/profile">Profile</Link>
          </p>


          <p>
            <Link to="/dashboard/settings">Settings</Link>
          </p>
        </nav>
      </aside>


      <main style={{ padding: "20px", flex: 1 }}>
        <Outlet />
      </main>
    </div>
  );
}


export default Dashboard;
