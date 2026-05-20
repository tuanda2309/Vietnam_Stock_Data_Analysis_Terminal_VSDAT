function MiniMetric({ label, value }) {
  return (
    <div className='bg-[#0A0F24]/60 border border-slate-800 rounded-lg p-3'>
      <p className='text-[11px] uppercase tracking-wider text-slate-500 font-bold'>{label}</p>
      <p className='text-sm md:text-base font-extrabold text-slate-100 mt-1 break-words'>{value}</p>
    </div>
  );
}

export default MiniMetric;
