import { useParams, useSearchParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../../services/api';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Skeleton } from '../../components/ui/Skeleton';
import { formatCurrency } from '../../utils/formatCurrency';

export default function AccountantProfileView() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const jobId = searchParams.get('job_id');

  const { data, isLoading } = useQuery({
    queryKey: ['accountant', id, jobId],
    queryFn: async () => {
      const response = await api.get('/accountants/' + id + '/profile?job_id=' + jobId);
      return response.data.data;
    },
    enabled: !!jobId,
  });

  if (isLoading) return <div className="container"><Skeleton height="300px" /></div>;
  if (!data) return <div className="container"><p>Accountant not found.</p></div>;

  return (
    <div className="container" style={{ padding: '32px 24px', maxWidth: 720, margin: '0 auto' }}>
      <Link to={'/client/jobs/' + jobId} style={{ fontSize: 14 }}>Back to Bids</Link>
      <h1 style={{ marginTop: 16 }}>{data.name}</h1>
      <p style={{ color: 'var(--color-text-muted)', marginBottom: 24 }}>{data.email}</p>

      <div style={{ display: 'flex', gap: 16, marginBottom: 24 }}>
        <Card padding="md" style={{ flex: 1 }}>
          <h3 style={{ color: 'var(--color-primary)', fontSize: 20, marginBottom: 4 }}>
            {formatCurrency(data.bid_price, 'USD')}
          </h3>
          <p style={{ fontSize: 12, color: 'var(--color-text-muted)' }}>Bid Amount</p>
        </Card>
        <Card padding="md" style={{ flex: 1 }}>
          <h3 style={{ color: 'var(--color-primary)', fontSize: 20, marginBottom: 4 }}>
            {data.years_of_experience || 'N/A'}
          </h3>
          <p style={{ fontSize: 12, color: 'var(--color-text-muted)' }}>Years Experience</p>
        </Card>
        <Card padding="md" style={{ flex: 1 }}>
          <h3 style={{ color: 'var(--color-primary)', fontSize: 20, marginBottom: 4 }}>
            {data.bid_delivery || 'N/A'}
          </h3>
          <p style={{ fontSize: 12, color: 'var(--color-text-muted)' }}>Delivery Time</p>
        </Card>
      </div>

      {data.bio && (
        <Card padding="lg" style={{ marginBottom: 16 }}>
          <h3 style={{ marginBottom: 8 }}>Bio</h3>
          <p style={{ color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>{data.bio}</p>
        </Card>
      )}

      <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
        <Card padding="lg" style={{ flex: 1 }}>
          <h3 style={{ marginBottom: 12 }}>Certifications</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {data.certifications && data.certifications.length > 0
              ? data.certifications.map(function(c, i) { return <Badge key={i} variant={c.custom ? 'neutral' : 'primary'}>{c.name}</Badge>; })
              : <p style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>None listed</p>
            }
          </div>
        </Card>
        <Card padding="lg" style={{ flex: 1 }}>
          <h3 style={{ marginBottom: 12 }}>Software Skills</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {data.software_skills && data.software_skills.length > 0
              ? data.software_skills.map(function(s, i) { return <Badge key={i} variant="neutral">{s}</Badge>; })
              : <p style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>None listed</p>
            }
          </div>
        </Card>
      </div>

      <Card padding="lg">
        <h3 style={{ marginBottom: 12 }}>Jurisdictions and Standards</h3>
        <div style={{ display: 'flex', gap: 24 }}>
          <div>
            <p style={{ fontSize: 12, color: 'var(--color-text-muted)', marginBottom: 4 }}>Jurisdictions</p>
            <div style={{ display: 'flex', gap: 4 }}>
              {data.jurisdictions_served && data.jurisdictions_served.length > 0
                ? data.jurisdictions_served.map(function(j, i) { return <Badge key={i} variant="success">{j}</Badge>; })
                : <span style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>None</span>
              }
            </div>
          </div>
          <div>
            <p style={{ fontSize: 12, color: 'var(--color-text-muted)', marginBottom: 4 }}>Standards</p>
            <div style={{ display: 'flex', gap: 4 }}>
              {data.accounting_standards && data.accounting_standards.length > 0
                ? data.accounting_standards.map(function(s, i) { return <Badge key={i} variant="warning">{s}</Badge>; })
                : <span style={{ fontSize: 13, color: 'var(--color-text-muted)' }}>None</span>
              }
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
