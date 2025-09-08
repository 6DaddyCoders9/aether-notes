import Button from "../components/Button";
import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function DashboardPage() {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token");

    if (token) {
      // Save token once
      localStorage.setItem("token", token);

      // Remove token from URL (clean it up)
      navigate("/dashboard", { replace: true });
    }
  }, [location, navigate]);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r flex flex-col p-4">
        {/* Logo */}
        <h1 className="text-2xl font-bold text-blue-600 mb-6">
          AetherNotes
        </h1>

        {/* Navigation */}
        <nav className="flex flex-col gap-3 flex-grow">
          <a href="#" className="text-gray-700 hover:text-blue-600">
            📄 My Notes
          </a>
          <a href="#" className="text-gray-700 hover:text-blue-600">
            📂 Shared
          </a>
          <a href="#" className="text-gray-700 hover:text-blue-600">
            ⚙️ Settings
          </a>
        </nav>

        {/* User Section */}
        <div className="mt-auto">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-gray-300"></div>
            <span className="text-gray-700">User</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-semibold text-gray-800">
            Welcome back 👋
          </h2>
          <Button>+ New Note</Button>
        </div>

        {/* Placeholder Notes */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="p-4 bg-white rounded-lg shadow hover:shadow-md transition"
            >
              <h3 className="font-semibold text-gray-800 mb-2">
                Note {i}
              </h3>
              <p className="text-sm text-gray-600">
                This is a placeholder note. Later, this will load from DB.
              </p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
