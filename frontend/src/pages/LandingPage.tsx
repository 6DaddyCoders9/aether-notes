import { Link } from "react-router-dom";
import Logo from "../assets/logo.png";
import Button from "../components/Button";

export default function LandingPage() {
  return (
    <div className="flex h-screen flex-col items-center justify-center bg-gray-50 text-center px-4">
      {/* Logo */}
      <img src={Logo} alt="AetherNotes Logo" className="w-20 h-20 mb-6" />

      {/* Title */}
      <h1 className="text-4xl font-bold text-gray-800 mb-2">
        AetherNotes
      </h1>

      {/* Tagline */}
      <p className="text-lg text-gray-600 mb-8 max-w-md">
        A smarter way to capture knowledge. Collaborate, and keep your notes accessible everywhere.
      </p>

      {/* CTA Button */}
      <Link to="/login">
        <Button>Get Started</Button>
      </Link>
    </div>
  );
}
