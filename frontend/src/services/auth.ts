import api from "./api"; // we’ll define api.ts if not done yet

export async function requestOtp(email: string) {
  return api.post("/auth/otp/request", { email });
}

export async function verifyOtp(email: string, otp: string) {
  return api.post("/auth/otp/verify", { email, otp });
}

export async function loginWithGoogle() {
  window.location.href = `${import.meta.env.VITE_API_BASE_URL}/auth/google/login`;
}
