function Header() {
  return (
    <header className='mb-10 border-b border-slate-800 pb-8 flex flex-col items-center text-center'>
      <div className='relative mb-5 group'>
        <div className='absolute -inset-1 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-full blur opacity-40 group-hover:opacity-70 transition duration-500'></div>
        <img
          src='/cat-logo.png'
          alt='Cat Intelligence Logo'
          className='relative w-24 h-24 md:w-28 md:h-28 rounded-full object-cover border-2 border-slate-700 bg-[#131A35] p-1 shadow-2xl'
        />
      </div>

      <h1 className='text-3xl md:text-4xl lg:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent px-4 max-w-3xl'>
        Vietnam Stock Data Analysis Terminal (VSDAT)
      </h1>
      <p className='text-slate-400 text-sm md:text-base mt-3 max-w-xl font-medium px-4 leading-relaxed'>
        Hệ thống phân tích kỹ thuật nâng cao và định lượng chuỗi thời gian thị trường chứng khoán Việt Nam
      </p>
    </header>
  );
}

export default Header;
