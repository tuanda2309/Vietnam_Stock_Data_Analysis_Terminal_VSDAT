function InfoRow({ label, value, valueClass = 'text-slate-100' }) {
  return (
    <div className='flex items-center justify-between gap-3 py-2 border-b border-slate-800/70 last:border-0'>
      <span className='text-sm text-slate-400'>{label}</span>
      <span className={`text-sm font-bold text-right ${valueClass}`}>{value}</span>
    </div>
  );
}

export default InfoRow;
