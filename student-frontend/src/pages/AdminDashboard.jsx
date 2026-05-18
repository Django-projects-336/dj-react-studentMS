import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

// Admin dashboard: list all students, approve pending ones, delete students.
function AdminDashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [students, setStudents] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  // Load the student list when page opens
  useEffect(() => {
    fetchStudents();
  }, []);

  async function fetchStudents() {
    setLoading(true);
    setError("");

    try {
      const response = await api.get("/admin/students/");
      setStudents(response.data);
    } catch (err) {
      setError("Could not load students. Are you logged in as admin?");
    } finally {
      setLoading(false);
    }
  }

  async function handleApprove(studentId) {
    setMessage("");
    try {
      await api.post(`/admin/students/${studentId}/approve/`);
      setMessage("Student approved.");
      fetchStudents();
    } catch (err) {
      setError("Could not approve student.");
    }
  }

  async function handleDelete(studentId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this student?"
    );
    if (!confirmed) return;

    setMessage("");
    try {
      await api.delete(`/admin/students/${studentId}/delete/`);
      setMessage("Student deleted.");
      fetchStudents();
    } catch (err) {
      setError("Could not delete student.");
    }
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="page-card page-card-wide">
      <div className="dashboard-header">
        <div>
          <h1>Admin Dashboard</h1>
          <p className="subtitle">Welcome, {user?.username}</p>
        </div>
        <button type="button" className="btn-secondary" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}
      {message && <p className="success-message">{message}</p>}

      {loading ? (
        <p>Loading students...</p>
      ) : students.length === 0 ? (
        <p>No students registered yet.</p>
      ) : (
        <div className="table-wrapper">
          <table className="student-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Name</th>
                <th>Course</th>
                <th>Branch</th>
                <th>Year</th>
                <th>Approved</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td>{student.username}</td>
                  <td>{student.name}</td>
                  <td>{student.course}</td>
                  <td>{student.branch}</td>
                  <td>{student.course_year}</td>
                  <td>{student.is_approved ? "Yes" : "No"}</td>
                  <td className="actions-cell">
                    {!student.is_approved && (
                      <button
                        type="button"
                        className="btn-approve"
                        onClick={() => handleApprove(student.id)}
                      >
                        Approve
                      </button>
                    )}
                    <button
                      type="button"
                      className="btn-delete"
                      onClick={() => handleDelete(student.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default AdminDashboard;
