import { FaGithub } from "react-icons/fa";
import { MdEmail } from "react-icons/md";

export default function Footer() {
  return (
    <footer className="bg-gray-50 border-t">
      <div className="max-w-7xl mx-auto px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Left: Copyright */}
        <div className="flex-row items-center gap-5">
        <p className="text-sm text-gray-500">
          © {new Date().getFullYear()} Aether Notes. All rights reserved.
        </p>
        <a className="text-sm text-gray-500">
          Privacy Policy
        </a>
        </div>

        {/* Right: Icons */}
        <div className="flex items-center gap-5 text-gray-600">
          <a
            href="mailto:aethernotes@example.com"
            className="hover:text-black transition"
            aria-label="Email us"
          >
            <MdEmail size={40} />
          </a>

          <a
            href="https://github.com/6DaddyCoders9/aether-notes"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-black transition"
            aria-label="GitHub repository"
          >
            <FaGithub size={40} />
          </a>
        </div>
      </div>
    </footer>
  );
}
