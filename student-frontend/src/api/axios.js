import axios from "axios";

// Base URL for our Django API (all routes start with /api/)
const API_BASE_URL = "http://127.0.0.1:8000/api";

// Create one shared axios instance for the whole app.
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Before every request, attach the JWT access token if we have one saved.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
