import { Gauge } from 'lucide-react';

function SignalCard({ signal, actionStyle }) {
  return (
    <div className={`rounded-2xl border ${actionStyle.border} ${actionStyle.bg} p-5 md:p-6 shadow-xl`}>
      <div className='flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5'>
        <div className='space-y-3'>
          <div className='flex items-center gap-3 flex-wrap'>
            <span className={`px-4 py-2 rounded-full text-sm font-black tracking-widest ${actionStyle.badge}`}>
              {signal.action || 'CHƯA CÓ TÍN HIỆU'}
            </span>
            <span className='text-slate-400 text-sm font-medium'>Độ tin cậy</span>
            <span className={`text-2xl font-extrabold ${actionStyle.text}`}>{signal.confidence ?? '--'}%</span>
          </div>
          <h2 className='text-2xl md:text-3xl font-extrabold text-slate-100'>
            {signal.title || 'Chưa có tín hiệu'}
          </h2>
          <p className='text-slate-300 max-w-3xl leading-relaxed'>
            {signal.summary || 'Backend chưa trả về tín hiệu phân tích cho mã này.'}
          </p>
        </div>
        <div className='bg-[#0A0F24]/60 border border-slate-800 rounded-xl p-4 min-w-[220px]'>
          <div className='flex items-center gap-2 text-slate-400 text-xs uppercase font-bold tracking-wider mb-2'>
            <Gauge className='h-4 w-4' />
            Tóm tắt nhanh
          </div>
          <p className='text-sm text-slate-300'>Không có tín hiệu nào đảm bảo thắng. Luôn đặt điểm cắt lỗ trước khi vào lệnh.</p>
        </div>
      </div>
    </div>
  );
}

export default SignalCard;
