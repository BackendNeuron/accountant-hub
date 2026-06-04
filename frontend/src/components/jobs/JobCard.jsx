
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { JobMeta } from './JobMeta';
import './JobCard.css';

export function JobCard({ job }) {
  const { t } = useTranslation();
  const isClosed = job.status === 'closed';

  return (
    <Link to={`/jobs/${job.id}`} className="job-card-link">
      <Card hoverable padding="md" className={isClosed ? 'job-card-closed' : ''}>
        <div className="job-card-header">
          <Badge variant={isClosed ? 'danger' : 'success'}>{t(`jobCard.${job.status}`)}</Badge>
        </div>
        <h3 className="job-card-title">{job.title}</h3>
        <p className="job-card-company">{job.company_name || 'Company'}</p>
        <p className="job-card-desc">{job.description?.substring(0, 120)}...</p>
        <div className="job-card-tags">
          {job.category && <Badge variant="neutral">{job.category.name}</Badge>}
          {job.jurisdiction && <Badge variant="neutral">{job.jurisdiction}</Badge>}
        </div>
        <JobMeta job={job} />
      </Card>
    </Link>
  );
}
