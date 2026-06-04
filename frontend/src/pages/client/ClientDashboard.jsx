
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { clientService } from '../../services/profileService';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Skeleton } from '../../components/ui/Skeleton';
import { formatRelativeDate } from '../../utils/formatDate';
import './DashboardPage.css';

export default function ClientDashboard() {
  const { t } = useTranslation();
  const { data, isLoading } = useQuery({
    queryKey: ['my-jobs'],
    queryFn: () => clientService.getMyJobs(),
  });

  const jobs = data?.data || [];

  return (
    <div className="dashboard-page container">
      <div className="dash-header">
        <h1>{t('dashboard.title')}</h1>
        <Link to="/client/jobs/new"><Button variant="primary">{t('nav.postJob')}</Button></Link>
      </div>

      <div className="stats-grid">
        <Card padding="lg"><h3>{jobs.length}</h3><p>{t('dashboard.totalJobs')}</p></Card>
        <Card padding="lg"><h3>{jobs.filter((j) => j.status === 'open').length}</h3><p>{t('dashboard.activeJobs')}</p></Card>
        <Card padding="lg"><h3>{jobs.reduce((sum, j) => sum + (j.bids_count || 0), 0)}</h3><p>{t('dashboard.bidsReceived')}</p></Card>
      </div>

      <h2>My Jobs</h2>
      {isLoading ? <Skeleton height="200px" /> : jobs.length === 0 ? (
        <Card padding="lg"><p>No jobs posted yet. <Link to="/client/jobs/new">Post your first job</Link></p></Card>
      ) : (
        jobs.map((job) => (
          <Card key={job.id} padding="md" className="bid-row">
            <div>
              <Link to={`/client/jobs/${job.id}`}><strong>{job.title}</strong></Link>
              <span className="text-muted"> · {formatRelativeDate(job.posted_date)}</span>
            </div>
            <div className="bid-row-meta">
              <Badge variant={job.status === 'open' ? 'success' : 'danger'}>{job.status}</Badge>
              <span>{job.bids_count || 0} bids</span>
              <Link to={`/client/jobs/${job.id}/edit`}><Button variant="ghost" size="sm">{t('common.edit')}</Button></Link>
            </div>
          </Card>
        ))
      )}
    </div>
  );
}
