
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { clientService } from '../../services/profileService';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Skeleton } from '../../components/ui/Skeleton';
import { formatCurrency } from '../../utils/formatCurrency';
import './DashboardPage.css';

export default function ClientJobDetailPage() {
  const { id } = useParams();
  const { t } = useTranslation();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['job-bids', id],
    queryFn: () => clientService.getJobBids(id),
  });

  const bids = data || [];

  const acceptMutation = useMutation({
    mutationFn: (bidId) => clientService.acceptBid(id, bidId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['job-bids', id] }),
  });

  const rejectMutation = useMutation({
    mutationFn: (bidId) => clientService.rejectBid(id, bidId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['job-bids', id] }),
  });

  if (isLoading) return <Skeleton height="300px" />;

  return (
    <div className="dashboard-page container">
      <Link to="/client/dashboard">← Back</Link>
      <h1>Bids Received</h1>
      {bids.length === 0 ? (
        <Card padding="lg"><p>No bids yet.</p></Card>
      ) : (
        bids.map((bid) => (
          <Card key={bid.id} padding="lg" className="bid-detail-card">
            <div className="bid-detail-header">
              <Link to={`/accountant/${bid.accountant_id}?job_id=${id}`} style={{ color: 'var(--color-primary)', fontWeight: 600 }}>
                {bid.accountant_name || `Accountant #${bid.accountant_id}`}
              </Link>
              
              <Badge variant={bid.status === 'accepted' ? 'success' : bid.status === 'rejected' ? 'danger' : 'warning'}>{bid.status}</Badge>
            </div>
            <h3>{formatCurrency(bid.price, bid.currency)} — {bid.pricing_model}</h3>
            <p>{bid.proposal_letter?.substring(0, 300)}...</p>
            <div className="bid-detail-meta">
              <span>Delivery: {bid.delivery_time}</span>
              <span>Hours: {bid.estimated_hours || '—'}</span>
            </div>
            {bid.status === 'pending' && (
              <div className="bid-actions">
                <Button variant="primary" onClick={() => acceptMutation.mutate(bid.id)} loading={acceptMutation.isPending}>Accept</Button>
                <Button variant="danger" onClick={() => rejectMutation.mutate(bid.id)} loading={rejectMutation.isPending}>Reject</Button>
              </div>
            )}
          </Card>
        ))
      )}
    </div>
  );
}
