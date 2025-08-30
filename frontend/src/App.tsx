import { Link } from "react-router-dom";


export default function App() {
  return (
    <div>
      <h1 className="text-4xl font-bold text-red-500">Home</h1>
      <Link to="/login">Login</Link>
      <Link to="/dashboard">Dashboard</Link>
    </div>
  );
}
