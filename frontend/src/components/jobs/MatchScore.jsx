
import { useTranslation } from 'react-i18next';
import './MatchScore.css';

export function MatchScore({ data }) {
  const { t } = useTranslation();
  if (!data) return null;

  const { score, matched, missing, warnings } = data;
  const color = score >= 70 ? 'var(--color-primary)' : score >= 40 ? 'var(--color-warning)' : 'var(--color-danger)';

  return (
    <div className="match-score">
      <h4>{t('jobDetail.matchScore')}</h4>
      <div className="match-circle" style={{ borderColor: color, color }}>
        <span className="match-number">{score}%</span>
      </div>
      {matched?.length > 0 && <div className="match-list match-matched">{matched.map((m, i) => <div key={i}>✅ {m}</div>)}</div>}
      {missing?.length > 0 && <div className="match-list match-missing">{missing.map((m, i) => <div key={i}>⚠️ {m}</div>)}</div>}
      {warnings?.length > 0 && <div className="match-list match-warnings">{warnings.map((w, i) => <div key={i}>❗ {w}</div>)}</div>}
    </div>
  );
}
