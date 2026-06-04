import { useQuery } from '@tanstack/react-query';
import { jobService } from '../../services/jobService';
import { Skeleton } from '../../components/ui/Skeleton';

export default function PrivacyPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['content', 'privacy_policy'],
    queryFn: () => jobService.getContent('privacy_policy'),
  });

  return (
    <div className="container" style={{ padding: '40px 24px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>{data?.title || 'Privacy Policy'}</h1>
      {isLoading ? <Skeleton height="300px" /> : (
        <div style={{ whiteSpace: 'pre-line', lineHeight: 1.8, marginTop: 24 }}>{data?.body}</div>
      )}
    </div>
  );
}
