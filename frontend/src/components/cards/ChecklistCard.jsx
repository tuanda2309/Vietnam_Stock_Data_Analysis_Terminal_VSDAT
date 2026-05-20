import { AlertTriangle, CheckCircle2 } from 'lucide-react';

function ChecklistCard({ title, icon, items, emptyText, type }) {
  const isPositive = type === 'positive';
  return (
    <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg'>
      <div className='flex items-center gap-2 border-b border-slate-800 pb-3 mb-4'>
        {icon}
        <h3 className='text-sm font-bold uppercase tracking-wider text-slate-300'>{title}</h3>
      </div>
      {items.length === 0 ? (
        <p className='text-sm text-slate-500'>{emptyText}</p>
      ) : (
        <ul className='space-y-3'>
          {items.map((item, index) => (
            <li key={`${title}-${index}`} className='flex items-start gap-2 text-sm leading-relaxed text-slate-300'>
              {isPositive ? (
                <CheckCircle2 className='h-4 w-4 text-emerald-400 shrink-0 mt-0.5' />
              ) : (
                <AlertTriangle className='h-4 w-4 text-amber-400 shrink-0 mt-0.5' />
              )}
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ChecklistCard;
