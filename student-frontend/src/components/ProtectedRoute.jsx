import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

// Wraps pages that require the user to be logged in.
// allowedRole can be "student" or "admin" to block the wrong role.
function ProtectedRoute({ children, allowedRole }) {
  const { isAuthenticated, user } = useAuth();

  // No token? Send to login page.
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Student trying to open admin page? Send them to their dashboard.
  if (allowedRole === "admin" && user.isStudent) {
    return <Navigate to="/student-dashboard" replace />;
  }

  // Admin trying to open student page? Send them to admin dashboard.
  if (allowedRole === "student" && !user.isStudent) {
    return <Navigate to="/admin-dashboard" replace />;
  }

  return children;
}

export default ProtectedRoute;
