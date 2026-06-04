
import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';

import { useTranslation } from 'react-i18next';
import { jobService } from '../../services/jobService';
import { bidService } from '../../services/bidService';
import { useAuth } from '../../hooks/useAuth';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import { Skeleton } from '../../components/ui/Skeleton';
import { Modal } from '../../components/ui/Modal';
import { DisclaimerBanner } from '../../components/ui/DisclaimerBanner';
import { BidForm } from '../../components/jobs/BidForm';
import { MatchScore } from '../../components/jobs/MatchScore';
import { formatBudgetRange } from '../../utils/formatCurrency';
import { formatDeadline, formatRelativeDate } from '../../utils/formatDate';
import './JobDetailPage.css';

export default function JobDetailPage() {
  const { id } = useParams();
  const { t } = useTranslation();
  const queryClient = useQueryClient();

  const { isAuthenticated, role } = useAuth();
  const [bidModalOpen, setBidModalOpen] = useState(false);
  const [ndaAccepted, setNdaAccepted] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ['job', id],
    queryFn: () => jobService.getJob(id),
  });

  const { data: matchData } = useQuery({
    queryKey: ['job', id, 'match-score'],
    queryFn: () => bidService.getMatchScore(id),
    enabled: isAuthenticated && role === 'accountant',
  });

  const { data: ndaContent } = useQuery({
    queryKey: ['content', 'nda_default_text'],
    queryFn: () => jobService.getContent('nda_default_text'),
    enabled: data?.job?.nda_required && !ndaAccepted,
  });

  if (isLoading) return <div className="container"><Skeleton height="400px" variant="rect" /></div>;

  const job = data?.job;
  const currentUserBid = data?.current_user_bid;
  const isClosed = job?.status === 'closed';
  const isAccountant = isAuthenticated && role === 'accountant';
  const hasBid = !!currentUserBid;

  const handleNdaAccept = async () => {
      if (!isAuthenticated) {
          window.location.href = '/login';
          return;
      }
      try {
          await bidService.acceptNda(id);
          setNdaAccepted(true);
      } catch (err) {
          if (err.response?.status === 401 || err.response?.status === 403) {
              window.location.href = '/login';
          }
      }
  };

  return (
    <div className="job-detail-page container">
      <Link to="/" className="back-link">← {t('common.back')}</Link>

{job?.nda_required && !ndaAccepted ? (
    <div className="disclaimer-banner animate-fade-in">
      <div className="disclaimer-content">
        <h3>{t('jobDetail.ndaRequired')}</h3>
        <div className="disclaimer-text">
          {!isAuthenticated 
            ? 'You must login as an accountant to accept the NDA and view full job details.'
            : role !== 'accountant'
              ? 'Only accountants can accept NDAs. Please login with an accountant account to view full details and submit bids.'
              : (ndaContent?.body || 'You must accept the NDA to view full job details.')
          }
        </div>
        <div className="disclaimer-actions">
          {isAuthenticated && role === 'accountant' && (
            <Button variant="primary" onClick={handleNdaAccept}>
              {t('jobDetail.acceptNda')}
            </Button>
          )}
          {!isAuthenticated && (
            <Button variant="primary" onClick={() => window.location.href = '/login'}>
              {t('nav.login')}
            </Button>
          )}
          <Button variant="ghost" onClick={() => window.history.back()}>
            {t('common.back')}
          </Button>
        </div>
      </div>
    </div>
) : (
        <div className="job-detail-layout">
          <div className="job-detail-main">
            <div className="job-detail-header">
              <Badge variant={isClosed ? 'danger' : 'success'}>{t(`jobCard.${job?.status}`)}</Badge>
              <h1>{job?.title}</h1>
              <p className="job-company">{job?.company_name || 'Company'}</p>
              <div className="job-meta-row">
                <span>📅 {t('jobCard.posted')} {formatRelativeDate(job?.posted_date)}</span>
                <span>⏰ {t('jobCard.deadline')}: {formatDeadline(job?.deadline)}</span>
              </div>
            </div>

            <div className="job-description">
              <h2>Description</h2>
              <p>{job?.description}</p>
            </div>

            {job?.required_skills?.length > 0 && (
              <div className="job-tags">
                <h3>{t('jobDetail.requiredSkills')}</h3>
                <div className="tag-list">
                  {job.required_skills.map((s) => <Badge key={s} variant="neutral">{s}</Badge>)}
                </div>
              </div>
            )}

            {job?.required_certifications?.length > 0 && (
              <div className="job-tags">
                <h3>{t('jobDetail.certifications')}</h3>
                <div className="tag-list">
                  {job.required_certifications.map((c) => <Badge key={c} variant="primary">{c}</Badge>)}
                </div>
              </div>
            )}
          </div>

          <div className="job-detail-sidebar">
            <Card padding="lg">
              <div className="sidebar-budget">{formatBudgetRange(job?.budget_min, job?.budget_max, job?.currency)}</div>
              <div className="sidebar-meta">
                <div><strong>{t('jobDetail.delivery')}:</strong> {job?.expected_delivery_time || '—'}</div>
                <div><strong>{t('jobDetail.bidsReceived')}:</strong> {job?.bids_count || 0}</div>
                <div><strong>{t('jobDetail.standard')}:</strong> {job?.accounting_standard || '—'}</div>
                <div><strong>{t('jobDetail.jurisdiction')}:</strong> {job?.jurisdiction || '—'}</div>
              </div>

              {isAccountant && matchData && <MatchScore data={matchData} />}

              {isAccountant && !hasBid && !isClosed && (
                <Button variant="primary" size="lg" onClick={() => setBidModalOpen(true)} className="btn-full">
                  {t('jobDetail.submitBid')}
                </Button>
              )}

              {isAccountant && hasBid && (
                <Card variant="success" padding="md">
                  <p>✅ {t('jobDetail.alreadyBid')}</p>
                  <p className="text-sm">Proposed: {formatBudgetRange(currentUserBid?.price, currentUserBid?.price, job?.currency)}</p>
                </Card>
              )}

              {isClosed && (
                <Card variant="closed" padding="md">
                  <p>🔒 {t('jobDetail.jobClosed')}</p>
                </Card>
              )}

              {!isAuthenticated && (
                <Link to="/login">
                  <Button variant="primary" size="lg" className="btn-full">{t('nav.login')} to {t('jobDetail.submitBid')}</Button>
                </Link>
              )}
            </Card>
          </div>
        </div>
      )}

      <Modal isOpen={bidModalOpen} onClose={() => setBidModalOpen(false)} title={t('bidForm.title')}>
        <BidForm jobId={parseInt(id)} jobCurrency={job?.currency} onSuccess={() => {
            setBidModalOpen(false);
            queryClient.invalidateQueries({ queryKey: ['job', id] });
        }} />
      </Modal>
    </div>
  );
}
