import { Loader2 } from 'lucide-react';

function LoadingState({ loading }) {
  if (!loading) return null;

  return (
    <div className='flex flex-col items-center justify-center p-20 bg-[#131A35] rounded-xl border border-slate-800 shadow-xl'>
      <Loader2 className='h-12 w-12 text-emerald-500 animate-spin mb-4' />
      <p className='text-slate-400 font-medium'>Hệ thống đang tải dữ liệu và tính toán định lượng chỉ báo...</p>
    </div>
  );
}

export default LoadingState;
