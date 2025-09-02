import { Navigate } from "react-router-dom";

type ProtectedRouteProps = {
  children: React.ReactNode;
};

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const token = localStorage.getItem("token");

  if (!token) {
    // not logged in → redirect to login
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
