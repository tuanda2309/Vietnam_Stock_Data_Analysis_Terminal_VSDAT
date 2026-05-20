import { AlertTriangle, ListChecks } from 'lucide-react';

import Header from './components/layout/Header';
import RiskWarning from './components/layout/RiskWarning';
import ErrorAlert from './components/layout/ErrorAlert';
import LoadingState from './components/layout/LoadingState';
import SearchPanel from './components/controls/SearchPanel';
import ExportPanel from './components/controls/ExportPanel';
import PriceCard from './components/cards/PriceCard';
import RsiCard from './components/cards/RsiCard';
import Ma20Card from './components/cards/Ma20Card';
import SignalCard from './components/cards/SignalCard';
import RiskManagementCard from './components/cards/RiskManagementCard';
import LevelsCard from './components/cards/LevelsCard';
import MarketCard from './components/cards/MarketCard';
import SuggestedOrderCard from './components/cards/SuggestedOrderCard';
import TechnicalMetricsCard from './components/cards/TechnicalMetricsCard';
import ChecklistCard from './components/cards/ChecklistCard';
import PriceVolumeChart from './components/charts/PriceVolumeChart';
import RsiChart from './components/charts/RsiChart';
import MacdChart from './components/charts/MacdChart';
import { ACTION_STYLES } from './constants/actionStyles';
import { useStockAnalysis } from './hooks/useStockAnalysis';
import { useLanguage } from './i18n/LanguageContext';

function App() {
  const {
    symbol,
    startDate,
    endDate,
    stockData,
    loading,
    exporting,
    error,
    handleSymbolChange,
    getStock,
    exportExcel,
    setStartDate,
    setEndDate,
  } = useStockAnalysis();

  const { t } = useLanguage();

  const technical = stockData?.technical || {};
  const levels = stockData?.levels || {};
  const riskManagement = stockData?.riskManagement || {};
  const market = stockData?.market || {};
  const signal = stockData?.signal || {};
  const suggestedOrder = stockData?.suggestedOrder || {};
  const reasons = Array.isArray(stockData?.reasons) ? stockData.reasons : [];
  const warnings = Array.isArray(stockData?.warnings) ? stockData.warnings : [];

  const statusColorClass = stockData?.status === 'up'
    ? 'text-emerald-400'
    : stockData?.status === 'down'
      ? 'text-rose-400'
      : 'text-amber-400';

  const actionStyle = ACTION_STYLES[signal?.action] || ACTION_STYLES.DEFAULT;
  const entryZone = riskManagement?.entryZone || {};
  const takeProfitZone = riskManagement?.takeProfitZone || {};
  const riskRewardRatio = riskManagement?.riskRewardRatio;
  const riskRewardWeak = riskRewardRatio !== null && riskRewardRatio !== undefined && Number(riskRewardRatio) < 1.5;

  return (
    <div className='notranslate min-h-screen bg-[#0A0F24] text-slate-100 p-4 md:p-10 font-sans antialiased' translate='no'>
      <div className='max-w-7xl mx-auto'>
        <Header />

        <div className='grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6 items-stretch'>
          <SearchPanel
            symbol={symbol}
            handleSymbolChange={handleSymbolChange}
            getStock={getStock}
            loading={loading}
          />
          <ExportPanel
            startDate={startDate}
            endDate={endDate}
            setStartDate={setStartDate}
            setEndDate={setEndDate}
            exportExcel={exportExcel}
            exporting={exporting}
          />
        </div>

        <RiskWarning />
        <ErrorAlert error={error} />
        <LoadingState loading={loading} />

        {stockData && !loading && (
          <div className='space-y-6 animate-fadeIn'>
            <div className='grid grid-cols-1 md:grid-cols-3 gap-5'>
              <PriceCard stockData={stockData} statusColorClass={statusColorClass} />
              <RsiCard technical={technical} stockData={stockData} />
              <Ma20Card technical={technical} stockData={stockData} />
            </div>

            <SignalCard signal={signal} actionStyle={actionStyle} />

            <div className='grid grid-cols-1 lg:grid-cols-3 gap-5'>
              <RiskManagementCard
                riskManagement={riskManagement}
                entryZone={entryZone}
                takeProfitZone={takeProfitZone}
                riskRewardRatio={riskRewardRatio}
                riskRewardWeak={riskRewardWeak}
              />
              <LevelsCard levels={levels} />
              <MarketCard market={market} />
            </div>

            <div className='grid grid-cols-1 lg:grid-cols-3 gap-5'>
              <SuggestedOrderCard suggestedOrder={suggestedOrder} />

              <div className='lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-5'>
                <ChecklistCard
                  title={t('checklist.positiveReasons')}
                  icon={<ListChecks className='h-4 w-4 text-emerald-400' />}
                  items={reasons}
                  emptyText={t('checklist.noPositiveReasons')}
                  type='positive'
                />
                <ChecklistCard
                  title={t('checklist.warnings')}
                  icon={<AlertTriangle className='h-4 w-4 text-amber-400' />}
                  items={warnings}
                  emptyText={t('checklist.noWarnings')}
                  type='warning'
                />
              </div>
            </div>

            <TechnicalMetricsCard technical={technical} />

            <PriceVolumeChart
              stockData={stockData}
              levels={levels}
              riskManagement={riskManagement}
              takeProfitZone={takeProfitZone}
            />
            <RsiChart stockData={stockData} />
            <MacdChart stockData={stockData} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
