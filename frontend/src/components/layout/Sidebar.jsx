import { useTranslation } from 'react-i18next';
import './Sidebar.css';

export function Sidebar({ filters, onFilterChange, onClear, isOpen, onClose }) {
  const { t } = useTranslation();

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={'sidebar ' + (isOpen ? 'sidebar-open' : '')}>
        <div className="sidebar-header">
          <h3>{t('filters.title')}</h3>
          <button className="sidebar-close" onClick={onClose}>X</button>
        </div>
        <div className="sidebar-body">
          <div className="filter-group">
            <label className="filter-label">{t('filters.category')}</label>
            <select className="input-field select-field"
              value={filters.category || ''}
              onChange={(e) => onFilterChange('category', e.target.value)}>
              <option value="">{t('filters.all')}</option>
              {filters.categories && filters.categories.map((cat) => (
                <option key={cat.slug} value={cat.slug}>{cat.name}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label">{t('filters.budgetRange')}</label>
            <div className="filter-range">
              <input type="number" className="input-field" placeholder="Min"
                value={filters.budget_min || ''} onChange={(e) => onFilterChange('budget_min', e.target.value)} />
              <span>-</span>
              <input type="number" className="input-field" placeholder="Max"
                value={filters.budget_max || ''} onChange={(e) => onFilterChange('budget_max', e.target.value)} />
            </div>
          </div>

          <div className="filter-group">
            <label className="filter-label">{t('filters.standard')}</label>
            <select className="input-field select-field"
              value={filters.accounting_standard || ''}
              onChange={(e) => onFilterChange('accounting_standard', e.target.value)}>
              <option value="">{t('filters.all')}</option>
              <option value="GAAP">GAAP</option>
              <option value="IFRS">IFRS</option>
              <option value="Local GAAP">Local GAAP</option>
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label">{t('filters.jurisdiction')}</label>
            <input type="text" className="input-field" placeholder="US, UK, UAE..."
              value={filters.jurisdiction || ''} onChange={(e) => onFilterChange('jurisdiction', e.target.value)} />
          </div>

          <div className="filter-group">
            <label className="filter-label">{t('filters.status')}</label>
            <select className="input-field select-field"
              value={filters.status || ''}
              onChange={(e) => onFilterChange('status', e.target.value)}>
              <option value="">{t('filters.all')}</option>
              <option value="open">{t('filters.openOnly')}</option>
              <option value="closed">{t('filters.closedOnly')}</option>
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label">{t('filters.sortBy')}</label>
            <select className="input-field select-field"
              value={filters.sort || 'newest'}
              onChange={(e) => onFilterChange('sort', e.target.value)}>
              <option value="newest">{t('filters.newest')}</option>
              <option value="budget_high">{t('filters.highestBudget')}</option>
              <option value="bids">{t('filters.mostBids')}</option>
            </select>
          </div>
        </div>
        <div className="sidebar-footer">
          <button className="btn btn-ghost btn-md" onClick={onClear}>{t('filters.clearAll')}</button>
        </div>
      </aside>
    </>
  );
}
