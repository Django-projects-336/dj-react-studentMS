import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

// Student dashboard: read-only view of the logged-in student's profile.
function StudentDashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProfile() {
      try {
        const response = await api.get("/profile/");
        setProfile(response.data);
      } catch (err) {
        setError("Could not load your profile.");
      } finally {
        setLoading(false);
      }
    }

    fetchProfile();
  }, []);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  if (loading) {
    return <div className="page-card">Loading profile...</div>;
  }

  if (error) {
    return (
      <div className="page-card">
        <p className="error-message">{error}</p>
        <button onClick={handleLogout}>Logout</button>
      </div>
    );
  }

  return (
    <div className="page-card page-card-wide">
      <div className="dashboard-header">
        <div>
          <h1>Student Dashboard</h1>
          <p className="subtitle">Welcome, {user?.username}</p>
        </div>
        <button type="button" className="btn-secondary" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <p className="info-note">
        Your profile is read-only. Contact admin if details are wrong.
      </p>

      <div className="profile-grid">
        <ProfileField label="Username" value={profile.username} />
        <ProfileField label="Email" value={profile.email} />
        <ProfileField label="Name" value={profile.name} />
        <ProfileField label="Age" value={profile.age} />
        <ProfileField label="Phone" value={profile.phone_number} />
        <ProfileField label="Gender" value={profile.gender} />
        <ProfileField label="Father's name" value={profile.fathers_name} />
        <ProfileField label="Course" value={profile.course} />
        <ProfileField label="Branch" value={profile.branch} />
        <ProfileField label="Course year" value={profile.course_year} />
        <ProfileField
          label="Approved"
          value={profile.is_approved ? "Yes" : "No"}
        />
      </div>
    </div>
  );
}

function ProfileField({ label, value }) {
  return (
    <div className="profile-field">
      <span className="field-label">{label}</span>
      <span className="field-value">{value}</span>
    </div>
  );
}

export default StudentDashboard;
