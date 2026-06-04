
import { useTranslation } from 'react-i18next';
import { formatBudgetRange } from '../../utils/formatCurrency';
import { formatDeadline, formatRelativeDate } from '../../utils/formatDate';
import './JobMeta.css';

export function JobMeta({ job }) {
  const { t } = useTranslation();
  return (
    <div className="job-meta">
      <span className="job-meta-budget">💰 {formatBudgetRange(job.budget_min, job.budget_max, job.currency)}</span>
      <span>📅 {formatDeadline(job.deadline)}</span>
      <span>📝 {job.bids_count || 0} {t('jobCard.bids')}</span>
      <span className="job-meta-date">{formatRelativeDate(job.posted_date)}</span>
    </div>
  );
}
