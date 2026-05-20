import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

import { useLanguage } from '../../i18n/LanguageContext';

function RsiChart({ stockData }) {
  const { t } = useLanguage();

  return (
    <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
      <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>{t('chart.rsiTitle')}</h3>
      <div className='h-[170px] w-full'>
        <ResponsiveContainer width='100%' height='100%'>
          <LineChart data={stockData.data || []} margin={{ top: 5, right: 5, left: -15, bottom: 0 }}>
            <CartesianGrid strokeDasharray='3 3' stroke='#1E264A' />
            <XAxis dataKey='time' stroke='#64748B' fontSize={11} tickLine={false} />
            <YAxis domain={[0, 100]} ticks={[30, 50, 70]} stroke='#64748B' fontSize={11} />
            <Tooltip contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px' }} />
            <ReferenceLine y={30} stroke='#60A5FA' strokeDasharray='4 4' />
            <ReferenceLine y={50} stroke='#94A3B8' strokeDasharray='4 4' />
            <ReferenceLine y={70} stroke='#F43F5E' strokeDasharray='4 4' />
            <Line type='monotone' dataKey='RSI' name={t('chart.rsi')} stroke='#F43F5E' strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default RsiChart;
