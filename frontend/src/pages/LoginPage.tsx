import { useState } from "react";
import AuthCard from "../components/AuthCard";
import Input from "../components/Input";
import Button from "../components/Button";
import GoogleLogo from "../assets/gogle-logo.png";
import { requestOtp, verifyOtp, loginWithGoogle } from "../services/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState<"email" | "otp">("email");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSendOtp(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await requestOtp(email);
      setStep("otp");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to send OTP");
    } finally {
      setLoading(false);
    }
  }

  async function handleVerifyOtp(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await verifyOtp(email, otp);
      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/dashboard";
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to verify OTP");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen items-center justify-center bg-gray-50 px-4">
      <AuthCard>
        {/* Title */}
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Sign in to AetherNotes
        </h2>

        {/* Google Login */}
        <Button type="button"
        onClick={loginWithGoogle}
        className="flex items-center gap-2 bg-white hover:bg-gray-200 w-full h-10 border rounded-md"
        >
          <img src={GoogleLogo} alt="Google Logo" className="w-5 h-5 ml-2" />
          <span className="text-gray-700">Continue with Google</span>
        </Button>

        {/* Divider */}
        <div className="flex items-center my-6">
          <hr className="flex-grow border-gray-300" />
          <span className="px-2 text-sm text-gray-500">or</span>
          <hr className="flex-grow border-gray-300" />
        </div>

        {/* Email OTP Form */}
        {step === "email" && (
          <form onSubmit={handleSendOtp} className="flex flex-col gap-4">
            <Input
              type="email"
              placeholder="Enter your email"
              label="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Button type="submit" disabled={loading}>
              {loading ? "Sending..." : "Send OTP"}
            </Button>
          </form>
        )}

        {step === "otp" && (
          <form onSubmit={handleVerifyOtp} className="flex flex-col gap-4">
            <Input
              type="text"
              placeholder="Enter OTP"
              label="One-Time Passcode"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              required
            />
            <Button type="submit" disabled={loading}>
              {loading ? "Verifying..." : "Verify OTP"}
            </Button>
          </form>
        )}

        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
      </AuthCard>
    </div>
  );
}
