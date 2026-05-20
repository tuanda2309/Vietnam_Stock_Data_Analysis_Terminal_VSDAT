import { Bar, CartesianGrid, ComposedChart, Legend, Line, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

function MacdChart({ stockData }) {
  return (
    <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
      <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>MACD - Xu hướng động lượng</h3>
      <div className='h-[240px] w-full'>
        <ResponsiveContainer width='100%' height='100%'>
          <ComposedChart data={stockData.data || []} margin={{ top: 5, right: 5, left: -15, bottom: 0 }}>
            <CartesianGrid strokeDasharray='3 3' stroke='#1E264A' />
            <XAxis dataKey='time' stroke='#64748B' fontSize={11} tickLine={false} />
            <YAxis stroke='#64748B' fontSize={11} />
            <Tooltip contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px' }} />
            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
            <ReferenceLine y={0} stroke='#64748B' strokeDasharray='4 4' />
            <Bar dataKey='MACD_Histogram' name='Histogram' fill='#64748B' opacity={0.35} radius={[2, 2, 0, 0]} />
            <Line type='monotone' dataKey='MACD' name='MACD' stroke='#34D399' strokeWidth={2} dot={false} />
            <Line type='monotone' dataKey='Signal_Line' name='Signal' stroke='#F59E0B' strokeWidth={2} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default MacdChart;
