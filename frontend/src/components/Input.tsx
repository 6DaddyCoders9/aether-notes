type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
};

export default function Input({ label, ...props }: InputProps) {
  return (
    <div className="flex flex-col gap-1">
      {label && <label className="text-sm font-medium">{label}</label>}
      <input
        className="px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 outline-none"
        {...props}
      />
    </div>
  );
}
