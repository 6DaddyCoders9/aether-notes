import { Link } from "react-router-dom";
import HeroBg from "../../assets/hero-bg.jpg";

export default function Hero() {
  return (
    <section
      className="relative h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: `url(${HeroBg})` }}
    >
      {/* Visual layer (plane/clouds placeholder) */}
      <div className="absolute inset-0 pointer-events-none">
        {/* Future animation goes here */}
      </div>

      {/* Text + CTA */}
      <div className="text-center z-10 px-4">
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-4">
          Aether Notes
        </h1>
        <p className="text-lg md:text-xl text-white mb-6">
          Organize, search and ask questions across your documents.
        </p>
        <Link
          to="/login"
          className="px-6 py-3 rounded-md bg-black text-white hover:bg-gray-800 transition"
        >
          Get Started
        </Link>
      </div>
    </section>
  );
}