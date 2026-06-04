
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { bidService } from '../../services/bidService';
import { useAuth } from '../../hooks/useAuth';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Skeleton } from '../../components/ui/Skeleton';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatRelativeDate } from '../../utils/formatDate';
import './DashboardPage.css';

export default function AccountantDashboard() {
  const { t } = useTranslation();
  const { user } = useAuth();

  const { data: bidsData, isLoading } = useQuery({
    queryKey: ['my-bids'],
    queryFn: () => bidService.getMyBids(),
  });

  const bids = bidsData?.data || [];
  const pending = bids.filter((b) => b.status === 'pending').length;
  const accepted = bids.filter((b) => b.status === 'accepted').length;

  return (
    <div className="dashboard-page container">
      <h1>{t('dashboard.title')}</h1>
      <div className="stats-grid">
        <Card padding="lg"><h3>{bids.length}</h3><p>{t('dashboard.totalBids')}</p></Card>
        <Card padding="lg"><h3>{pending}</h3><p>{t('dashboard.pendingBids')}</p></Card>
        <Card padding="lg"><h3>{accepted}</h3><p>{t('dashboard.acceptedBids')}</p></Card>
        <Card padding="lg"><h3>—</h3><p>{t('dashboard.profileComplete')}</p></Card>
      </div>

      <h2>{t('dashboard.recentBids')}</h2>
      {isLoading ? (
        <Skeleton height="200px" variant="rect" />
      ) : bids.length === 0 ? (
        <Card padding="lg"><p>{t('common.noBids')}</p><Link to="/">{t('nav.browseJobs')}</Link></Card>
      ) : (
        <div className="bids-table">
          {bids.slice(0, 10).map((bid) => (
            <Card key={bid.id} padding="md" className="bid-row">
              <div>
                <Link to={`/jobs/${bid.job_id}`}><strong>Job #{bid.job_id}</strong></Link>
                <span className="text-muted"> · {formatRelativeDate(bid.created_at)}</span>
              </div>
              <div className="bid-row-meta">
                <span>{formatCurrency(bid.price, bid.currency)}</span>
                <Badge variant={bid.status === 'accepted' ? 'success' : bid.status === 'rejected' ? 'danger' : 'warning'}>{bid.status}</Badge>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
