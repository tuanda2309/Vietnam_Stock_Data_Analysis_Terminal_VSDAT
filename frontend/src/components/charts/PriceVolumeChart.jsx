import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import { useLanguage } from '../../i18n/LanguageContext';
import { formatCurrency } from '../../utils/formatters';

function PriceVolumeChart({ stockData, levels, riskManagement, takeProfitZone }) {
  const { t } = useLanguage();

  return (
    <div className='bg-[#131A35] p-4 md:p-6 rounded-xl border border-slate-800 shadow-lg'>
      <h3 className='text-base font-bold text-slate-300 mb-4 uppercase tracking-wider'>{t('chart.priceVolumeTitle')}</h3>
      <div className='h-[420px] w-full'>
        <ResponsiveContainer width='100%' height='100%'>
          <ComposedChart data={stockData.data || []} margin={{ top: 10, right: 5, left: -15, bottom: 0 }}>
            <CartesianGrid strokeDasharray='3 3' stroke='#1E264A' />
            <XAxis dataKey='time' stroke='#64748B' fontSize={11} tickLine={false} />
            <YAxis
              yAxisId='price'
              domain={[(dataMin) => Math.floor(dataMin * 0.98), (dataMax) => Math.ceil(dataMax * 1.02)]}
              stroke='#64748B'
              fontSize={11}
              orientation='left'
              tickFormatter={(v) => Number(v).toLocaleString('vi-VN')}
            />
            <YAxis yAxisId='volume' domain={['0', 'dataMax * 4']} orientation='right' hide />
            <Tooltip
              contentStyle={{ backgroundColor: '#0D132E', borderColor: '#1E264A', borderRadius: '8px', color: '#fff' }}
              formatter={(value, name) => {
                if (value === null || value === undefined) return ['--', name];
                return [name === t('chart.volume') ? Number(value).toLocaleString('vi-VN') : formatCurrency(value), name];
              }}
            />
            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
            {levels.supportNearest && <ReferenceLine yAxisId='price' y={levels.supportNearest} stroke='#22C55E' strokeDasharray='4 4' label={{ value: t('chart.support'), fill: '#22C55E', fontSize: 11 }} />}
            {levels.resistanceNearest && <ReferenceLine yAxisId='price' y={levels.resistanceNearest} stroke='#F59E0B' strokeDasharray='4 4' label={{ value: t('chart.resistance'), fill: '#F59E0B', fontSize: 11 }} />}
            {riskManagement.stopLoss && <ReferenceLine yAxisId='price' y={riskManagement.stopLoss} stroke='#EF4444' strokeDasharray='4 4' label={{ value: t('chart.stopLoss'), fill: '#EF4444', fontSize: 11 }} />}
            {takeProfitZone.from && <ReferenceLine yAxisId='price' y={takeProfitZone.from} stroke='#A78BFA' strokeDasharray='4 4' label={{ value: t('chart.takeProfit'), fill: '#A78BFA', fontSize: 11 }} />}
            <Bar yAxisId='volume' dataKey='volume' name={t('chart.volume')} fill='#3B82F6' opacity={0.15} radius={[2, 2, 0, 0]} />
            <Line yAxisId='price' type='monotone' dataKey='close' name={t('chart.closePrice')} stroke='#34D399' strokeWidth={2.5} dot={false} />
            <Line yAxisId='price' type='monotone' dataKey='MA20' name='MA20' stroke='#60A5FA' strokeWidth={1.5} dot={false} />
            <Line yAxisId='price' type='monotone' dataKey='MA50' name='MA50' stroke='#F59E0B' strokeWidth={1.5} dot={false} />
            <Line yAxisId='price' type='monotone' dataKey='MA100' name='MA100' stroke='#EC4899' strokeWidth={1.5} dot={false} />
            <Line yAxisId='price' type='monotone' dataKey='MA200' name='MA200' stroke='#8B5CF6' strokeWidth={1.5} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default PriceVolumeChart;
