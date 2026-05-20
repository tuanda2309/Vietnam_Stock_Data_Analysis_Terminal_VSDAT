function SectionCard({ title, icon, children }) {
  return (
    <div className='bg-[#131A35] p-5 rounded-xl border border-slate-800 shadow-lg'>
      <div className='flex items-center gap-2 border-b border-slate-800 pb-3 mb-4'>
        {icon}
        <h3 className='text-sm font-bold uppercase tracking-wider text-slate-300'>{title}</h3>
      </div>
      {children}
    </div>
  );
}

export default SectionCard;
