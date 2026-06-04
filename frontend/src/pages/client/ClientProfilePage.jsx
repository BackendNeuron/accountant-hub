import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '../../hooks/useAuth';
import { profileService } from '../../services/profileService';
import { Input } from '../../components/ui/Input';
import { Textarea } from '../../components/ui/Textarea';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import './ProfilePage.css';

export default function ClientProfilePage() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    company_name: '', company_industry: '', website: '', company_description: '',
    company_size: '', city: '',
  });
  const [saved, setSaved] = useState(false);

  const { data: profileData } = useQuery({
    queryKey: ['my-profile'],
    queryFn: profileService.getProfile,
  });

  useEffect(() => {
    if (profileData?.profile) {
      setForm({
        company_name: profileData.profile.company_name || '',
        company_industry: profileData.profile.company_industry || '',
        website: profileData.profile.website || '',
        company_description: profileData.profile.company_description || '',
        company_size: profileData.profile.company_size || '',
        city: profileData.profile.city || '',
      });
    }
  }, [profileData]);

  const mutation = useMutation({
    mutationFn: (data) => profileService.updateProfile(data),
    onSuccess: () => {
      setSaved(true);
      queryClient.invalidateQueries({ queryKey: ['my-profile'] });
      setTimeout(() => setSaved(false), 3000);
    },
  });

  return (
    <div className="profile-page container">
      <h1>{user?.name}</h1>
      <Card padding="lg">
        <Input label="Company Name" value={form.company_name} onChange={(e) => setForm({...form, company_name: e.target.value})} />
        <Input label="Industry" value={form.company_industry} onChange={(e) => setForm({...form, company_industry: e.target.value})} />
        <Input label="Company Size" value={form.company_size} onChange={(e) => setForm({...form, company_size: e.target.value})} placeholder="1-10, 11-50, 51-200, 201+" />
        <Input label="Website" value={form.website} onChange={(e) => setForm({...form, website: e.target.value})} />
        <Input label="City" value={form.city} onChange={(e) => setForm({...form, city: e.target.value})} />
        <Textarea label="Description" value={form.company_description} onChange={(e) => setForm({...form, company_description: e.target.value})} rows={4} />
        <Button onClick={() => mutation.mutate(form)} loading={mutation.isPending}>Save</Button>
        {saved && <span className="saved-msg">Saved</span>}
      </Card>
    </div>
  );
}