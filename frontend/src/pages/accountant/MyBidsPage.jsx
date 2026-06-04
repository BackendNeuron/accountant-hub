
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { bidService } from '../../services/bidService';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Pagination } from '../../components/ui/Pagination';
import { EmptyState } from '../../components/ui/EmptyState';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatFullDate } from '../../utils/formatDate';
import './DashboardPage.css';

export default function MyBidsPage() {
  const { t } = useTranslation();
  const [page, setPage] = useState(1);

  const { data } = useQuery({
    queryKey: ['my-bids', page],
    queryFn: () => bidService.getMyBids(page),
  });

  const bids = data?.data || [];
  const totalPages = data?.meta?.last_page || 1;

  return (
    <div className="dashboard-page container">
      <h1>{t('nav.myBids')}</h1>
      {bids.length === 0 ? (
        <EmptyState title={t('common.noBids')} description="Start browsing jobs and submitting proposals" action={{ label: t('nav.browseJobs'), onClick: () => window.location.href = '/' }} />
      ) : (
        <>
          {bids.map((bid) => (
            <Card key={bid.id} padding="md" className="bid-row">
              <div className="bid-row-main">
                <Link to={`/jobs/${bid.job_id}`}><strong>Job #{bid.job_id}</strong></Link>
                <p className="text-muted">{formatFullDate(bid.created_at)}</p>
              </div>
              <div className="bid-row-meta">
                <strong>{formatCurrency(bid.price, bid.currency)}</strong>
                <Badge variant={bid.status === 'accepted' ? 'success' : bid.status === 'rejected' ? 'danger' : 'warning'}>{bid.status}</Badge>
              </div>
            </Card>
          ))}
          <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}
