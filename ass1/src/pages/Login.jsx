function Login() {
  return (
    <div>
      <h1>Login Page</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <div style={{ marginBottom: "10px" }}>
          <label htmlFor="username">Username: </label>
          <input id="username" type="text" placeholder="Enter username" />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <label htmlFor="password">Password: </label>
          <input id="password" type="password" placeholder="Enter password" />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Login;
