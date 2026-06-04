import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../hooks/useAuth';
import { profileService } from '../../services/profileService';
import { jobService } from '../../services/jobService';
import { Input } from '../../components/ui/Input';
import { Textarea } from '../../components/ui/Textarea';
import { MultiSelect } from '../../components/ui/MultiSelect';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';
import './ProfilePage.css';

function DocumentList() {
  const queryClient = useQueryClient();
  const { data: docs } = useQuery({
    queryKey: ['my-documents'],
    queryFn: profileService.getDocuments,
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => profileService.deleteDocument(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['my-documents'] }),
  });

  const documents = docs || [];
  if (documents.length === 0) return null;

  return (
    <div>
      <h3 style={{ fontSize: 15, marginBottom: 12 }}>Uploaded Documents</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {documents.map((doc) => (
          <div key={doc.id} style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '10px 14px', background: 'var(--color-bg-surface-2)',
            borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)',
          }}>
            <div>
              <span style={{ fontSize: 14, color: 'var(--color-text-primary)' }}>{doc.file_name}</span>
              <span style={{ fontSize: 11, color: 'var(--color-text-muted)', marginLeft: 12 }}>
                {doc.document_type} {doc.is_verified ? '- Verified' : ''}
              </span>
            </div>
            <Button size="sm" variant="danger" onClick={() => deleteMutation.mutate(doc.id)}>Delete</Button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function AccountantProfilePage() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState('profile');
  const [certSelected, setCertSelected] = useState([]);
  const [swSelected, setSwSelected] = useState([]);

  const { data: profileData } = useQuery({
    queryKey: ['my-profile'],
    queryFn: profileService.getProfile,
  });

  const { data: certifications } = useQuery({
    queryKey: ['certifications'],
    queryFn: jobService.getCertifications,
  });

  const [form, setForm] = useState({
    bio: '', years_of_experience: '', hourly_rate: '',
    jurisdictions_served: [], accounting_standards: [],
  });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (profileData?.profile) {
      setForm({
        bio: profileData.profile.bio || '',
        years_of_experience: profileData.profile.years_of_experience || '',
        hourly_rate: profileData.profile.hourly_rate || '',
        jurisdictions_served: profileData.profile.jurisdictions_served || [],
        accounting_standards: profileData.profile.accounting_standards || [],
      });
    }
  }, [profileData]);

  useEffect(() => {
    if (profileData?.profile?.certifications) {
      setCertSelected(profileData.profile.certifications || []);
    }
  }, [profileData]);

  useEffect(() => {
    if (profileData?.profile?.software_skills) {
      setSwSelected(profileData.profile.software_skills || []);
    }
  }, [profileData]);

  const updateMutation = useMutation({
    mutationFn: (data) => profileService.updateProfile(data),
    onSuccess: () => {
      setSaved(true);
      queryClient.invalidateQueries({ queryKey: ['my-profile'] });
      setTimeout(() => setSaved(false), 3000);
    },
  });

  const tabs = [
    { key: 'profile', label: 'Profile' },
    { key: 'certifications', label: 'Certifications' },
    { key: 'software', label: 'Software Skills' },
    { key: 'documents', label: 'Documents' },
  ];

  const certOptions = (certifications || []).map((c) => ({
    value: c.name,
    label: c.name,
  }));

  return (
    <div className="profile-page container">
      <h1>{user?.name}</h1>
      <p className="text-muted">{user?.email}</p>

      <div className="profile-tabs">
        {tabs.map((tab) => (
          <button key={tab.key} className={`profile-tab ${activeTab === tab.key ? 'active' : ''}`} onClick={() => setActiveTab(tab.key)}>{tab.label}</button>
        ))}
      </div>

      {activeTab === 'profile' && (
        <Card padding="lg">
          <Textarea label="Bio" value={form.bio} onChange={(e) => setForm({...form, bio: e.target.value})} rows={3} />
          <Input label="Years of Experience" type="number" value={form.years_of_experience} onChange={(e) => setForm({...form, years_of_experience: e.target.value})} />
          <Input label="Hourly Rate (USD)" type="number" value={form.hourly_rate} onChange={(e) => setForm({...form, hourly_rate: e.target.value})} />

          <MultiSelect
            label="Jurisdictions Served"
            options={[
              { value: 'US', label: 'United States' },
              { value: 'UK', label: 'United Kingdom' },
              { value: 'AE', label: 'UAE' },
              { value: 'SA', label: 'Saudi Arabia' },
              { value: 'QA', label: 'Qatar' },
              { value: 'KW', label: 'Kuwait' },
              { value: 'OM', label: 'Oman' },
              { value: 'BH', label: 'Bahrain' },
              { value: 'EG', label: 'Egypt' },
              { value: 'Global', label: 'Global' },
            ]}
            selected={form.jurisdictions_served || []}
            onChange={(val) => setForm({...form, jurisdictions_served: val})}
            placeholder="Select jurisdictions..."
          />

          <MultiSelect
            label="Accounting Standards"
            options={[
              { value: 'GAAP', label: 'US GAAP' },
              { value: 'IFRS', label: 'IFRS' },
              { value: 'Local GAAP', label: 'Local GAAP' },
            ]}
            selected={form.accounting_standards || []}
            onChange={(val) => setForm({...form, accounting_standards: val})}
            placeholder="Select standards..."
          />

          <Button onClick={() => updateMutation.mutate(form)} loading={updateMutation.isPending}>{t('common.save')}</Button>
          {saved && <span className="saved-msg">Saved</span>}
        </Card>
      )}

      {activeTab === 'certifications' && (
        <Card padding="lg">
          <p style={{ marginBottom: 16, color: 'var(--color-text-secondary)', fontSize: 13 }}>
            Select the certifications you hold. These will be used for job matching.
          </p>
          <MultiSelect
            label="Your Certifications"
            options={certOptions}
            selected={certSelected}
            onChange={setCertSelected}
            placeholder="Choose certifications..."
          />
          <div style={{ marginTop: 16 }}>
            <Button onClick={() => {
              profileService.updateCertifications({ certifications: certSelected }).then(() => {
                setSaved(true);
                setTimeout(() => setSaved(false), 3000);
              });
            }}>
              Save Certifications
            </Button>
            {saved && <span className="saved-msg">Saved</span>}
          </div>
        </Card>
      )}

      {activeTab === 'software' && (
        <Card padding="lg">
          <p style={{ marginBottom: 16, color: 'var(--color-text-secondary)', fontSize: 13 }}>
            Select the accounting software you are proficient in.
          </p>
          <MultiSelect
            label="Software Skills"
            options={[
              { value: 'QuickBooks', label: 'QuickBooks' },
              { value: 'Xero', label: 'Xero' },
              { value: 'SAP', label: 'SAP' },
              { value: 'Oracle NetSuite', label: 'Oracle NetSuite' },
              { value: 'Sage', label: 'Sage' },
              { value: 'Zoho Books', label: 'Zoho Books' },
              { value: 'FreshBooks', label: 'FreshBooks' },
              { value: 'Wave', label: 'Wave' },
              { value: 'Microsoft Dynamics GP', label: 'Microsoft Dynamics GP' },
              { value: 'Tally', label: 'Tally' },
              { value: 'Excel/Google Sheets', label: 'Excel/Google Sheets' },
              { value: 'Tableau', label: 'Tableau' },
              { value: 'Power BI', label: 'Power BI' },
              { value: 'Alteryx', label: 'Alteryx' },
            ]}
            selected={swSelected}
            onChange={setSwSelected}
            placeholder="Choose software..."
          />
          <div style={{ marginTop: 16 }}>
            <Button onClick={() => {
              profileService.updateSoftwareSkills({ software_skills: swSelected }).then(() => {
                setSaved(true);
                setTimeout(() => setSaved(false), 3000);
              });
            }}>
              Save Software Skills
            </Button>
            {saved && <span className="saved-msg">Saved</span>}
          </div>
        </Card>
      )}

      {activeTab === 'documents' && (
        <Card padding="lg">
          <p style={{ marginBottom: 20, color: 'var(--color-text-secondary)', fontSize: 13 }}>
            Upload your CV, certificates, and portfolio documents. Supported: PDF, DOC, DOCX, PNG, JPG (max 10MB).
          </p>

          <div style={{
            border: '2px dashed var(--color-border)',
            borderRadius: 'var(--radius-lg)',
            padding: '40px 24px',
            textAlign: 'center',
            marginBottom: 24,
            background: 'var(--color-bg-surface-2)',
            transition: 'border-color 0.2s',
            cursor: 'pointer',
          }}
            onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--color-primary)'}
            onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--color-border)'}
            onClick={() => document.getElementById('file-upload').click()}
          >
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--color-text-muted)" strokeWidth="1.5" style={{ marginBottom: 12 }}>
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
            </svg>
            <p style={{ fontSize: 14, color: 'var(--color-text-primary)', marginBottom: 4, fontWeight: 500 }}>
              Drag and drop your file here
            </p>
            <p style={{ fontSize: 12, color: 'var(--color-text-muted)', marginBottom: 16 }}>
              or click to browse
            </p>
            <span style={{
              display: 'inline-block',
              padding: '8px 20px',
              background: 'var(--color-primary)',
              color: 'white',
              borderRadius: 'var(--radius-md)',
              fontSize: 13,
              fontWeight: 500,
            }}>
              Choose File
            </span>
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.doc,.docx,.png,.jpg,.jpeg"
              style={{ display: 'none' }}
              onChange={async (e) => {
                const file = e.target.files[0];
                if (!file) return;
                const formData = new FormData();
                formData.append('file', file);
                formData.append('document_type', 'certificate_proof');
                try {
                  await profileService.uploadDocument(formData);
                  queryClient.invalidateQueries({ queryKey: ['my-documents'] });
                  setSaved(true);
                  setTimeout(() => setSaved(false), 3000);
                  e.target.value = '';
                } catch (err) {
                  alert('Upload failed: ' + (err.response?.data?.detail || 'Unknown error'));
                }
              }}
            />
          </div>

          {saved && <p style={{ color: 'var(--color-primary)', fontSize: 13, marginBottom: 16 }}>File uploaded successfully</p>}

          <DocumentList />
        </Card>
      )}
    </div>
  );
}