import api from "./api";

// 1. Request OTP to email
export async function requestOtp(email: string) {
  return api.post("/api/v1/auth/otp/request-otp", { email });
}

// 2. Verify OTP and get JWT
export async function verifyOtp(email: string, otp: string) {
  return api.post("/api/v1/auth/otp/verify-otp", { email, otp });
}

// 3. Redirect to Google Login
export function loginWithGoogle() {
  window.location.href = `${import.meta.env.VITE_API_BASE_URL}/api/v1/auth/google/login`;
}
