import { Link } from "react-router-dom";
import Logo from "../assets/favicon.png"; 

export default function Navbar() {
  return (
    <nav className="w-full fixed top-0 left-0 bg-white shadow-md z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-3">
        {/* Left: Logo */}
        <Link to="/" className="flex items-center gap-2">
          <img src={Logo} alt="Aether Notes Logo" className="w-10" />
          <span className="font-bold text-lg text-gray-800">Aether Notes</span>
        </Link>

        {/* Right: Log In button */}
        <Link
          to="/login"
          className="px-4 py-2 rounded-md bg-black text-white text-sm font-medium hover:bg-gray-800 transition"
        >
          Log In
        </Link>
      </div>
    </nav>
  );
}
