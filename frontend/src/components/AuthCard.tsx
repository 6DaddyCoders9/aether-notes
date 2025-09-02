type Props = { children: React.ReactNode };

export default function AuthCard({ children }: Props) {
  return (
    <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
      {children}
    </div>
  );
}
