import { AlertTriangle } from 'lucide-react';

function ErrorAlert({ error }) {
  if (!error) return null;

  return (
    <div className='bg-red-950/40 border border-red-900 text-red-200 p-4 rounded-lg mb-6 text-sm font-medium flex items-center gap-3 animate-fadeIn'>
      <AlertTriangle className='h-5 w-5 text-red-400 shrink-0' />
      <span>{error}</span>
    </div>
  );
}

export default ErrorAlert;
