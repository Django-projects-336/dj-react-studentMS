import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

// Login page: sends username/password to Django and saves JWT tokens.
function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Handle form submit
  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/login/", {
        username: username,
        password: password,
      });

      const { access, refresh, username: loggedInUser, is_student } =
        response.data;

      // Save tokens and user role in context + localStorage
      login(access, refresh, loggedInUser, is_student);

      // Redirect based on role
      if (is_student) {
        navigate("/student-dashboard");
      } else {
        navigate("/admin-dashboard");
      }
    } catch (err) {
      // Show error message from Django if login failed
      let message = "Login failed. Please check your username and password.";

      if (err.response?.data?.detail) {
        message = err.response.data.detail;
      } else if (err.response?.data?.non_field_errors) {
        message = err.response.data.non_field_errors[0];
      } else if (typeof err.response?.data === "object") {
        // ValidationError sometimes returns a list under a key
        const firstKey = Object.keys(err.response.data)[0];
        const firstValue = err.response.data[firstKey];
        if (Array.isArray(firstValue)) {
          message = firstValue[0];
        }
      }

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-card">
      <h1>Login</h1>
      <p className="subtitle">Sign in to your student or admin account</p>

      {error && <p className="error-message">{error}</p>}

      <form onSubmit={handleSubmit} className="form">
        <label>
          Username
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>

      <p className="link-text">
        New student? <Link to="/signup">Create an account</Link>
      </p>
    </div>
  );
}

export default Login;
