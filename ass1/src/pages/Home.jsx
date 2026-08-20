import { useNavigate } from "react-router-dom";


function Home() {
  const navigate = useNavigate();


  return (
    <div>
      <h1>Welcome to My App</h1>
      <p>Welcome! You have reached the home page.</p>


      <button onClick={() => navigate("/login")}>
        Go to Login
      </button>
    </div>
  );
}


export default Home;
