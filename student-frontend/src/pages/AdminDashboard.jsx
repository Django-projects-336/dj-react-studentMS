import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

// Empty form used when admin clicks "Add Student"
const EMPTY_FORM = {
  username: "",
  email: "",
  password: "",
  is_approved: true,
  name: "",
  age: "",
  phone_number: "",
  gender: "M",
  fathers_name: "",
  course: "",
  branch: "",
  course_year: "1st",
};

// Admin dashboard: full CRUD — Create, Read, Update, Delete students.
function AdminDashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [students, setStudents] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  // "none" = no form, "add" = create form, "edit" = update form
  const [formMode, setFormMode] = useState("none");
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);

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

  function handleFormChange(event) {
    const { name, value, type, checked } = event.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  }

  // Open blank form to create a new student
  function openAddForm() {
    setFormMode("add");
    setEditingId(null);
    setFormData(EMPTY_FORM);
    setError("");
    setMessage("");
  }

  // Fill form with existing student data to edit
  function openEditForm(student) {
    setFormMode("edit");
    setEditingId(student.id);
    setFormData({
      username: student.username,
      email: student.email || "",
      password: "",
      is_approved: student.is_approved,
      name: student.name,
      age: student.age,
      phone_number: student.phone_number,
      gender: student.gender,
      fathers_name: student.fathers_name,
      course: student.course,
      branch: student.branch,
      course_year: student.course_year,
    });
    setError("");
    setMessage("");
  }

  function closeForm() {
    setFormMode("none");
    setEditingId(null);
    setFormData(EMPTY_FORM);
  }

  // CREATE — POST new student
  async function handleCreate(event) {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      await api.post("/admin/students/", {
        ...formData,
        age: Number(formData.age),
      });
      setMessage("Student created successfully.");
      closeForm();
      fetchStudents();
    } catch (err) {
      setError(getErrorMessage(err, "Could not create student."));
    } finally {
      setSaving(false);
    }
  }

  // UPDATE — PUT changes to existing student
  async function handleUpdate(event) {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      const payload = {
        ...formData,
        age: Number(formData.age),
      };
      // Do not send empty password (keeps old password on server)
      if (!payload.password) {
        delete payload.password;
      }

      await api.put(`/admin/students/${editingId}/`, payload);
      setMessage("Student updated successfully.");
      closeForm();
      fetchStudents();
    } catch (err) {
      setError(getErrorMessage(err, "Could not update student."));
    } finally {
      setSaving(false);
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

  // DELETE — remove student
  async function handleDelete(studentId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this student?"
    );
    if (!confirmed) return;

    setMessage("");
    try {
      await api.delete(`/admin/students/${studentId}/`);
      setMessage("Student deleted.");
      if (editingId === studentId) closeForm();
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
        <div className="header-actions">
          <button type="button" className="btn-primary" onClick={openAddForm}>
            + Add Student
          </button>
          <button type="button" className="btn-secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}
      {message && <p className="success-message">{message}</p>}

      {/* CREATE or UPDATE form */}
      {formMode !== "none" && (
        <div className="admin-form-panel">
          <h2>{formMode === "add" ? "Add New Student" : "Edit Student"}</h2>

          <form
            onSubmit={formMode === "add" ? handleCreate : handleUpdate}
            className="form form-grid"
          >
            <label>
              Username
              <input
                name="username"
                value={formData.username}
                onChange={handleFormChange}
                required
              />
            </label>

            <label>
              Email
              <input
                name="email"
                type="email"
                value={formData.email}
                onChange={handleFormChange}
              />
            </label>

            <label>
              Password
              <input
                name="password"
                type="password"
                value={formData.password}
                onChange={handleFormChange}
                required={formMode === "add"}
                placeholder={
                  formMode === "edit" ? "Leave blank to keep current" : ""
                }
              />
            </label>

            <label className="checkbox-label">
              <input
                name="is_approved"
                type="checkbox"
                checked={formData.is_approved}
                onChange={handleFormChange}
              />
              Approved (can log in)
            </label>

            <label>
              Full name
              <input
                name="name"
                value={formData.name}
                onChange={handleFormChange}
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
                onChange={handleFormChange}
                required
              />
            </label>

            <label>
              Phone
              <input
                name="phone_number"
                value={formData.phone_number}
                onChange={handleFormChange}
                required
              />
            </label>

            <label>
              Gender
              <select
                name="gender"
                value={formData.gender}
                onChange={handleFormChange}
              >
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
                onChange={handleFormChange}
                required
              />
            </label>

            <label>
              Course
              <input
                name="course"
                value={formData.course}
                onChange={handleFormChange}
                required
              />
            </label>

            <label>
              Branch
              <input
                name="branch"
                value={formData.branch}
                onChange={handleFormChange}
                required
              />
            </label>

            <label>
              Course year
              <select
                name="course_year"
                value={formData.course_year}
                onChange={handleFormChange}
              >
                <option value="1st">1st</option>
                <option value="2nd">2nd</option>
                <option value="3rd">3rd</option>
                <option value="4th">4th</option>
              </select>
            </label>

            <div className="form-actions full-width">
              <button type="submit" disabled={saving}>
                {saving
                  ? "Saving..."
                  : formMode === "add"
                    ? "Create Student"
                    : "Save Changes"}
              </button>
              <button type="button" className="btn-secondary" onClick={closeForm}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {loading ? (
        <p>Loading students...</p>
      ) : students.length === 0 ? (
        <p>No students yet. Click &quot;Add Student&quot; to create one.</p>
      ) : (
        <div className="table-wrapper">
          <table className="student-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Name</th>
                <th>Email</th>
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
                  <td>{student.email}</td>
                  <td>{student.course}</td>
                  <td>{student.branch}</td>
                  <td>{student.course_year}</td>
                  <td>{student.is_approved ? "Yes" : "No"}</td>
                  <td className="actions-cell">
                    <button
                      type="button"
                      className="btn-edit"
                      onClick={() => openEditForm(student)}
                    >
                      Edit
                    </button>
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

// Pull a readable error string from Django's response
function getErrorMessage(err, fallback) {
  const data = err.response?.data;
  if (!data) return fallback;
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;
  const firstKey = Object.keys(data)[0];
  const firstValue = data[firstKey];
  if (Array.isArray(firstValue)) {
    return `${firstKey}: ${firstValue[0]}`;
  }
  return fallback;
}

export default AdminDashboard;
