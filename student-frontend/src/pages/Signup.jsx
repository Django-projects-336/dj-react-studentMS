import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

// Signup page: one form with user + profile fields (flat JSON like the API expects).
function Signup() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    name: "",
    age: "",
    phone_number: "",
    gender: "M",
    fathers_name: "",
    course: "",
    branch: "",
    course_year: "1st",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  // Update one field when user types in any input
  function handleChange(event) {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      await api.post("/signup/", {
        ...formData,
        age: Number(formData.age),
      });

      setSuccess(true);
    } catch (err) {
      const data = err.response?.data;
      let message = "Signup failed. Please check your details.";

      if (data && typeof data === "object") {
        const firstKey = Object.keys(data)[0];
        const firstValue = data[firstKey];
        if (Array.isArray(firstValue)) {
          message = `${firstKey}: ${firstValue[0]}`;
        }
      }

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  // After success, show a friendly message instead of the form
  if (success) {
    return (
      <div className="page-card success-card">
        <h1>Registration successful!</h1>
        <p className="success-message">
          Wait for admin approval before you can log in.
        </p>
        <Link to="/login" className="button-link">
          Go to Login
        </Link>
      </div>
    );
  }

  return (
    <div className="page-card page-card-wide">
      <h1>Student Signup</h1>
      <p className="subtitle">Create your account and profile</p>

      {error && <p className="error-message">{error}</p>}

      <form onSubmit={handleSubmit} className="form form-grid">
        <label>
          Username
          <input
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Email
          <input
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
          />
        </label>

        <label>
          Password
          <input
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Full name
          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Age
          <input
            name="age"
            type="number"
            min="1"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Phone number
          <input
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Gender
          <select name="gender" value={formData.gender} onChange={handleChange}>
            <option value="M">Male</option>
            <option value="F">Female</option>
            <option value="O">Other</option>
          </select>
        </label>

        <label>
          Father&apos;s name
          <input
            name="fathers_name"
            value={formData.fathers_name}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Course
          <input
            name="course"
            value={formData.course}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Branch
          <input
            name="branch"
            value={formData.branch}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Course year
          <select
            name="course_year"
            value={formData.course_year}
            onChange={handleChange}
          >
            <option value="1st">1st</option>
            <option value="2nd">2nd</option>
            <option value="3rd">3rd</option>
            <option value="4th">4th</option>
          </select>
        </label>

        <button type="submit" className="full-width" disabled={loading}>
          {loading ? "Submitting..." : "Sign up"}
        </button>
      </form>

      <p className="link-text">
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}

export default Signup;
