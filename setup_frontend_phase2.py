"""
Accountant Hub - Frontend Setup Phase II
All Pages: Public, Accountant, Client, Admin
Run: python setup_frontend_phase2.py
"""
import os
import py_compile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend", "src")
ERRORS = []
CREATED = []
MODIFIED = []

def write_file(rel_path, content):
    filepath = os.path.join(FRONTEND_DIR, rel_path)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    existed = os.path.exists(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    if existed:
        MODIFIED.append(filepath)
    else:
        CREATED.append(filepath)
    print(f"  {'🔧' if existed else '✅'} {'Updated' if existed else 'Created'}: {rel_path}")

def create_public_pages():
    """Step 1: Public pages"""
    print("\n" + "="*60)
    print("STEP 1: Public Pages (JobList, JobDetail, Login, Register)")
    print("="*60)

    write_file("pages/public/JobListPage.jsx", JOB_LIST_PAGE)
    write_file("pages/public/JobDetailPage.jsx", JOB_DETAIL_PAGE)
    write_file("pages/public/LoginPage.jsx", LOGIN_PAGE)
    write_file("pages/public/RegisterPage.jsx", REGISTER_PAGE)

def create_job_components():
    """Step 2: Job-specific components"""
    print("\n" + "="*60)
    print("STEP 2: Job Components (JobCard, JobMeta, BidForm, MatchScore)")
    print("="*60)

    write_file("components/jobs/JobCard.jsx", JOB_CARD)
    write_file("components/jobs/JobMeta.jsx", JOB_META)
    write_file("components/jobs/BidForm.jsx", BID_FORM)
    write_file("components/jobs/MatchScore.jsx", MATCH_SCORE)

def create_accountant_pages():
    """Step 3: Accountant pages"""
    print("\n" + "="*60)
    print("STEP 3: Accountant Pages (Dashboard, MyBids, Profile)")
    print("="*60)

    write_file("pages/accountant/AccountantDashboard.jsx", ACCOUNTANT_DASHBOARD)
    write_file("pages/accountant/MyBidsPage.jsx", MY_BIDS_PAGE)
    write_file("pages/accountant/AccountantProfilePage.jsx", ACCOUNTANT_PROFILE_PAGE)

def create_client_pages():
    """Step 4: Client pages"""
    print("\n" + "="*60)
    print("STEP 4: Client Pages (Dashboard, PostJob, EditJob, JobDetail, Profile)")
    print("="*60)

    write_file("pages/client/ClientDashboard.jsx", CLIENT_DASHBOARD)
    write_file("pages/client/PostJobPage.jsx", POST_JOB_PAGE)
    write_file("pages/client/EditJobPage.jsx", EDIT_JOB_PAGE)
    write_file("pages/client/ClientJobDetailPage.jsx", CLIENT_JOB_DETAIL_PAGE)
    write_file("pages/client/ClientProfilePage.jsx", CLIENT_PROFILE_PAGE)

def create_admin_pages():
    """Step 5: Admin pages"""
    print("\n" + "="*60)
    print("STEP 5: Admin Pages (Dashboard + all CRUD)")
    print("="*60)

    write_file("pages/admin/AdminDashboard.jsx", ADMIN_DASHBOARD)
    write_file("pages/admin/DataTable.jsx", DATA_TABLE)
    write_file("pages/admin/UsersPage.jsx", USERS_PAGE)
    write_file("pages/admin/JobsPage.jsx", ADMIN_JOBS_PAGE)
    write_file("pages/admin/BidsPage.jsx", ADMIN_BIDS_PAGE)
    write_file("pages/admin/CategoriesPage.jsx", ADMIN_CATEGORIES_PAGE)
    write_file("pages/admin/CertificationsPage.jsx", ADMIN_CERTIFICATIONS_PAGE)
    write_file("pages/admin/SoftwareSkillsPage.jsx", ADMIN_SOFTWARE_PAGE)
    write_file("pages/admin/CountriesPage.jsx", ADMIN_COUNTRIES_PAGE)
    write_file("pages/admin/DocumentsPage.jsx", ADMIN_DOCUMENTS_PAGE)
    write_file("pages/admin/ContentPage.jsx", ADMIN_CONTENT_PAGE)
    write_file("pages/admin/AuditLogsPage.jsx", ADMIN_AUDIT_LOGS_PAGE)

def update_app_routing():
    """Step 6: Update App.jsx with all routes"""
    print("\n" + "="*60)
    print("STEP 6: Update App.jsx with Complete Routing")
    print("="*60)

    write_file("App.jsx", APP_JSX_FULL)

def add_component_css():
    """Step 7: Add CSS files for all components"""
    print("\n" + "="*60)
    print("STEP 7: Component CSS Files")
    print("="*60)

    css_files = [
        ("components/ui/Button.css", BUTTON_CSS),
        ("components/ui/Input.css", INPUT_CSS),
        ("components/ui/Badge.css", BADGE_CSS),
        ("components/ui/Card.css", CARD_CSS),
        ("components/ui/Modal.css", MODAL_CSS),
        ("components/ui/Skeleton.css", SKELETON_CSS),
        ("components/ui/Pagination.css", PAGINATION_CSS),
        ("components/ui/SearchBar.css", SEARCHBAR_CSS),
        ("components/ui/EmptyState.css", EMPTYSTATE_CSS),
        ("components/ui/Toast.css", TOAST_CSS),
        ("components/ui/Spinner.css", SPINNER_CSS),
        ("components/ui/MultiSelect.css", MULTISELECT_CSS),
        ("components/ui/DisclaimerBanner.css", DISCLAIMER_CSS),
        ("components/layout/Navbar.css", NAVBAR_CSS),
        ("components/layout/Footer.css", FOOTER_CSS),
        ("components/layout/Sidebar.css", SIDEBAR_CSS),
        ("components/layout/Layout.css", LAYOUT_CSS),
    ]
    for filename, content in css_files:
        write_file(filename, content)

def print_summary():
    print("\n" + "="*60)
    print("FRONTEND PHASE II COMPLETE — ALL PAGES BUILT")
    print("="*60)
    print(f"\n📁 {len(CREATED)} files created")
    print(f"🔧 {len(MODIFIED)} files updated")
    print(f"\n✅ Ready to run: cd frontend && npm run dev")
    print(f"🌐 Open: http://localhost:5173")
    print("="*60)

# ============================================================
# PUBLIC PAGES
# ============================================================

JOB_LIST_PAGE = '''
import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { jobService } from '../../services/jobService';
import { useDebounce } from '../../hooks/useDebounce';
import { SearchBar } from '../../components/ui/SearchBar';
import { Pagination } from '../../components/ui/Pagination';
import { Skeleton } from '../../components/ui/Skeleton';
import { EmptyState } from '../../components/ui/EmptyState';
import { Sidebar } from '../../components/layout/Sidebar';
import { JobCard } from '../../components/jobs/JobCard';
import './JobListPage.css';

export default function JobListPage() {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    category: searchParams.get('category') || '',
    budget_min: searchParams.get('budget_min') || '',
    budget_max: searchParams.get('budget_max') || '',
    accounting_standard: searchParams.get('accounting_standard') || '',
    jurisdiction: searchParams.get('jurisdiction') || '',
    status: searchParams.get('status') || 'open',
    sort: searchParams.get('sort') || 'newest',
    page: parseInt(searchParams.get('page') || '1'),
  });

  const debouncedSearch = useDebounce(filters.search, 300);

  const { data, isLoading } = useQuery({
    queryKey: ['jobs', { ...filters, search: debouncedSearch }],
    queryFn: () => jobService.getJobs({ ...filters, search: debouncedSearch, per_page: 12 }),
  });

  const { data: categoriesData } = useQuery({
    queryKey: ['categories'],
    queryFn: jobService.getCategories,
  });

  useEffect(() => {
    const params = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value && value !== 'open') params[key] = value;
      else if (key === 'status' && value === 'open') params[key] = value;
    });
    if (filters.page > 1) params.page = filters.page;
    setSearchParams(params);
  }, [filters, setSearchParams]);

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
  };

  const clearFilters = () => {
    setFilters({
      search: '', category: '', budget_min: '', budget_max: '',
      accounting_standard: '', jurisdiction: '', status: 'open', sort: 'newest', page: 1,
    });
  };

  const jobs = data?.data || [];
  const total = data?.meta?.total || 0;
  const totalPages = data?.meta?.last_page || 1;

  return (
    <div className="job-list-page">
      <section className="hero">
        <h1 className="hero-title">{t('hero.title')}</h1>
        <p className="hero-subtitle">{t('hero.subtitle')}</p>
        <SearchBar
          value={filters.search}
          onChange={(v) => handleFilterChange('search', v)}
          placeholder={t('filters.search')}
        />
      </section>

      <div className="job-list-layout">
        <Sidebar
          filters={{ ...filters, categories: categoriesData || [] }}
          onFilterChange={handleFilterChange}
          onClear={clearFilters}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        <div className="job-list-main">
          <div className="job-list-topbar">
            <p className="job-count">{total} {total === 1 ? 'job' : 'jobs'} found</p>
            <button className="filter-toggle" onClick={() => setSidebarOpen(true)}>
              ☰ {t('filters.title')}
            </button>
          </div>

          {isLoading ? (
            <div className="job-list-grid">
              {[1,2,3,4,5,6].map((i) => <Skeleton key={i} height="180px" variant="rect" />)}
            </div>
          ) : jobs.length === 0 ? (
            <EmptyState
              title={t('common.noJobs')}
              description="Try adjusting your filters"
              action={{ label: t('filters.clearAll'), onClick: clearFilters }}
            />
          ) : (
            <div className="job-list-grid">
              {jobs.map((job) => <JobCard key={job.id} job={job} />)}
            </div>
          )}

          <Pagination page={filters.page} totalPages={totalPages} onPageChange={(p) => handleFilterChange('page', p)} />
        </div>
      </div>
    </div>
  );
}
'''

JOB_DETAIL_PAGE = '''
import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
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
    await bidService.acceptNda(id);
    setNdaAccepted(true);
  };

  return (
    <div className="job-detail-page container">
      <Link to="/" className="back-link">← {t('common.back')}</Link>

      {job?.nda_required && !ndaAccepted ? (
        <DisclaimerBanner
          title={t('jobDetail.ndaRequired')}
          text={ndaContent?.body || 'You must accept the NDA to view full job details.'}
          onAccept={handleNdaAccept}
          acceptLabel={t('jobDetail.acceptNda')}
          onDecline={() => window.history.back()}
          declineLabel={t('common.back')}
        />
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
        <BidForm jobId={parseInt(id)} jobCurrency={job?.currency} onSuccess={() => setBidModalOpen(false)} />
      </Modal>
    </div>
  );
}
'''

LOGIN_PAGE = '''
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../hooks/useAuth';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import './AuthPage.css';

export default function LoginPage() {
  const { t } = useTranslation();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await login(form.email, form.password);
      const role = res.user?.role;
      if (role === 'admin') navigate('/admin');
      else if (role === 'client') navigate('/client/dashboard');
      else navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card animate-fade-in">
        <Link to="/" className="auth-logo">Accountant<span className="logo-green">Hub</span></Link>
        <h1>{t('auth.loginTitle')}</h1>
        <form onSubmit={handleSubmit}>
          {error && <div className="auth-error">{error}</div>}
          <Input label={t('auth.email')} type="email" value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} required />
          <Input label={t('auth.password')} type="password" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} required />
          <Button type="submit" variant="primary" size="lg" loading={loading} className="btn-full">{t('auth.loginBtn')}</Button>
        </form>
        <p className="auth-footer">{t('auth.noAccount')} <Link to="/register">{t('auth.registerLink')}</Link></p>
      </div>
    </div>
  );
}
'''

REGISTER_PAGE = '''
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../hooks/useAuth';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import './AuthPage.css';

export default function RegisterPage() {
  const { t } = useTranslation();
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [role, setRole] = useState('accountant');
  const [form, setForm] = useState({ name: '', email: '', phone: '', password: '', company_name: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = { name: form.name, email: form.email, phone: form.phone, password: form.password, role };
      if (role === 'client') data.company_name = form.company_name;
      await registerUser(data);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card animate-fade-in">
        <Link to="/" className="auth-logo">Accountant<span className="logo-green">Hub</span></Link>
        <h1>{t('auth.registerTitle')}</h1>

        <div className="role-toggle">
          <button className={`role-btn ${role === 'accountant' ? 'active' : ''}`} onClick={() => setRole('accountant')}>{t('auth.accountantRole')}</button>
          <button className={`role-btn ${role === 'client' ? 'active' : ''}`} onClick={() => setRole('client')}>{t('auth.clientRole')}</button>
        </div>

        <form onSubmit={handleSubmit}>
          {error && <div className="auth-error">{error}</div>}
          <Input label={t('auth.fullName')} value={form.name} onChange={(e) => setForm({...form, name: e.target.value})} required />
          <Input label={t('auth.email')} type="email" value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} required />
          <Input label={t('auth.phone')} type="tel" value={form.phone} onChange={(e) => setForm({...form, phone: e.target.value})} required />
          {role === 'client' && <Input label={t('auth.companyName')} value={form.company_name} onChange={(e) => setForm({...form, company_name: e.target.value})} required />}
          <Input label={t('auth.password')} type="password" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} required minLength={8} />
          <Button type="submit" variant="primary" size="lg" loading={loading} className="btn-full">{t('auth.registerBtn')}</Button>
        </form>
        <p className="auth-footer">{t('auth.haveAccount')} <Link to="/login">{t('auth.loginLink')}</Link></p>
      </div>
    </div>
  );
}
'''

# ============================================================
# JOB COMPONENTS
# ============================================================

JOB_CARD = '''
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
'''

JOB_META = '''
import { useTranslation } from 'react-i18next';
import { formatBudgetRange } from '../../utils/formatCurrency';
import { formatDeadline, formatRelativeDate } from '../../utils/formatDate';
import './JobMeta.css';

export function JobMeta({ job }) {
  const { t } = useTranslation();
  return (
    <div className="job-meta">
      <span className="job-meta-budget">💰 {formatBudgetRange(job.budget_min, job.budget_max, job.currency)}</span>
      <span>📅 {formatDeadline(job.deadline)}</span>
      <span>📝 {job.bids_count || 0} {t('jobCard.bids')}</span>
      <span className="job-meta-date">{formatRelativeDate(job.posted_date)}</span>
    </div>
  );
}
'''

BID_FORM = '''
import { useState, useContext } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { bidService } from '../../services/bidService';
import { ToastContext } from '../../context/ToastContext';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { Textarea } from '../ui/Textarea';
import { Button } from '../ui/Button';
import { PRICING_MODELS } from '../../utils/constants';
import './BidForm.css';

export function BidForm({ jobId, jobCurrency = 'USD', onSuccess }) {
  const { t } = useTranslation();
  const { toast } = useContext(ToastContext);
  const queryClient = useQueryClient();
  const [errors, setErrors] = useState({});

  const [form, setForm] = useState({
    price: '',
    pricing_model: 'fixed',
    delivery_time: '',
    estimated_hours: '',
    proposal_letter: '',
    engagement_terms: '',
    services_included: ['Accounting Services'],
    includes_all_fees: true,
    jurisdiction_confirmed: false,
    terms_accepted: false,
  });

  const mutation = useMutation({
    mutationFn: (data) => bidService.submitBid(jobId, data),
    onSuccess: () => {
      toast.success(t('bidForm.success'));
      queryClient.invalidateQueries({ queryKey: ['job', String(jobId)] });
      queryClient.invalidateQueries({ queryKey: ['my-bids'] });
      onSuccess();
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || t('bidForm.error'));
    },
  });

  const validate = () => {
    const errs = {};
    if (!form.price || parseFloat(form.price) <= 0) errs.price = 'Required';
    if (!form.delivery_time) errs.delivery_time = 'Required';
    if (!form.proposal_letter || form.proposal_letter.length < 50) errs.proposal_letter = 'Min 50 characters';
    if (!form.jurisdiction_confirmed) errs.jurisdiction_confirmed = 'Required';
    if (!form.terms_accepted) errs.terms_accepted = 'Required';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    mutation.mutate({
      ...form,
      price: parseFloat(form.price),
      estimated_hours: form.estimated_hours ? parseInt(form.estimated_hours) : null,
    });
  };

  const update = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  return (
    <form className="bid-form" onSubmit={handleSubmit}>
      <Input label={t('bidForm.price')} type="number" prefix={jobCurrency} value={form.price} onChange={(e) => update('price', e.target.value)} error={errors.price} required />
      <Select label={t('bidForm.pricingModel')} options={PRICING_MODELS} value={form.pricing_model} onChange={(e) => update('pricing_model', e.target.value)} />
      <Input label={t('bidForm.deliveryTime')} value={form.delivery_time} onChange={(e) => update('delivery_time', e.target.value)} error={errors.delivery_time} placeholder="e.g. 2 weeks" required />
      <Input label={t('bidForm.estimatedHours')} type="number" value={form.estimated_hours} onChange={(e) => update('estimated_hours', e.target.value)} />
      <Textarea label={t('bidForm.coverLetter')} value={form.proposal_letter} onChange={(e) => update('proposal_letter', e.target.value)} rows={5} maxLength={2000} error={errors.proposal_letter} required />
      <Textarea label={t('bidForm.experience')} value={form.engagement_terms} onChange={(e) => update('engagement_terms', e.target.value)} rows={3} />

      <label className="checkbox-label">
        <input type="checkbox" checked={form.includes_all_fees} onChange={(e) => update('includes_all_fees', e.target.checked)} />
        {t('bidForm.allFeesIncluded')}
      </label>
      <label className="checkbox-label">
        <input type="checkbox" checked={form.jurisdiction_confirmed} onChange={(e) => update('jurisdiction_confirmed', e.target.checked)} />
        {t('bidForm.jurisdictionConfirm')}
        {errors.jurisdiction_confirmed && <span className="input-error-text">{errors.jurisdiction_confirmed}</span>}
      </label>
      <label className="checkbox-label">
        <input type="checkbox" checked={form.terms_accepted} onChange={(e) => update('terms_accepted', e.target.checked)} />
        {t('bidForm.termsAccept')}
        {errors.terms_accepted && <span className="input-error-text">{errors.terms_accepted}</span>}
      </label>

      <Button type="submit" variant="primary" size="lg" loading={mutation.isPending} className="btn-full">
        {t('bidForm.submit')}
      </Button>
    </form>
  );
}
'''

MATCH_SCORE = '''
import { useTranslation } from 'react-i18next';
import './MatchScore.css';

export function MatchScore({ data }) {
  const { t } = useTranslation();
  if (!data) return null;

  const { score, matched, missing, warnings } = data;
  const color = score >= 70 ? 'var(--color-primary)' : score >= 40 ? 'var(--color-warning)' : 'var(--color-danger)';

  return (
    <div className="match-score">
      <h4>{t('jobDetail.matchScore')}</h4>
      <div className="match-circle" style={{ borderColor: color, color }}>
        <span className="match-number">{score}%</span>
      </div>
      {matched?.length > 0 && <div className="match-list match-matched">{matched.map((m, i) => <div key={i}>✅ {m}</div>)}</div>}
      {missing?.length > 0 && <div className="match-list match-missing">{missing.map((m, i) => <div key={i}>⚠️ {m}</div>)}</div>}
      {warnings?.length > 0 && <div className="match-list match-warnings">{warnings.map((w, i) => <div key={i}>❗ {w}</div>)}</div>}
    </div>
  );
}
'''

# ============================================================
# ACCOUNTANT PAGES
# ============================================================

ACCOUNTANT_DASHBOARD = '''
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
'''

MY_BIDS_PAGE = '''
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
'''

ACCOUNTANT_PROFILE_PAGE = '''
import { useState } from 'react';
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
import { Badge } from '../../components/ui/Badge';
import './ProfilePage.css';

export default function AccountantProfilePage() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState('profile');

  const { data: profile } = useQuery({
    queryKey: ['my-profile'],
    queryFn: profileService.getProfile,
  });

  const { data: certifications } = useQuery({
    queryKey: ['certifications'],
    queryFn: jobService.getCertifications,
  });

  const [form, setForm] = useState({ bio: '', years_of_experience: '', hourly_rate: '' });
  const [saved, setSaved] = useState(false);

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
    { key: 'documents', label: 'Documents' },
  ];

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
          <Button onClick={() => updateMutation.mutate(form)} loading={updateMutation.isPending}>{t('common.save')}</Button>
          {saved && <span className="saved-msg">✅ Saved</span>}
        </Card>
      )}

      {activeTab === 'certifications' && (
        <Card padding="lg">
          <p>Certifications from: {certifications?.map((c) => c.name).join(', ') || 'Loading...'}</p>
          <MultiSelect
            label="Your Certifications"
            options={certifications?.map((c) => ({ value: c.name, label: c.name })) || []}
            selected={[]}
            onChange={() => {}}
          />
        </Card>
      )}

      {activeTab === 'documents' && (
        <Card padding="lg">
          <p>Upload your CV, certificates, and portfolio documents.</p>
          <input type="file" accept=".pdf,.doc,.docx,.png,.jpg" />
        </Card>
      )}
    </div>
  );
}
'''

# ============================================================
# CLIENT PAGES
# ============================================================

CLIENT_DASHBOARD = '''
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
'''

POST_JOB_PAGE = '''
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { clientService } from '../../services/profileService';
import { jobService } from '../../services/jobService';
import { Input } from '../../components/ui/Input';
import { Select } from '../../components/ui/Select';
import { Textarea } from '../../components/ui/Textarea';
import { Button } from '../../components/ui/Button';
import { PRICING_MODELS, ENGAGEMENT_TYPES } from '../../utils/constants';
import './PostJobPage.css';

export default function PostJobPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: jobService.getCategories });

  const [form, setForm] = useState({
    title: '', description: '', category_id: '', budget_min: '', budget_max: '',
    currency: 'USD', pricing_model: 'fixed', deadline: '', expected_delivery_time: '',
    engagement_type: 'one_time', jurisdiction: '', accounting_standard: '',
    nda_required: false,
  });

  const mutation = useMutation({
    mutationFn: (data) => clientService.createJob(data),
    onSuccess: (res) => {
      navigate('/client/dashboard');
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({
      ...form,
      category_id: parseInt(form.category_id),
      budget_min: parseFloat(form.budget_min),
      budget_max: parseFloat(form.budget_max),
    });
  };

  const update = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  const catOptions = (categories || []).map((c) => ({ value: c.id, label: c.name }));

  return (
    <div className="post-job-page container">
      <h1>Post a New Job</h1>
      <form onSubmit={handleSubmit} className="post-job-form">
        <Input label="Job Title" value={form.title} onChange={(e) => update('title', e.target.value)} required />
        <Select label="Category" options={catOptions} value={form.category_id} onChange={(e) => update('category_id', e.target.value)} required />
        <Textarea label="Description" value={form.description} onChange={(e) => update('description', e.target.value)} rows={6} required />

        <div className="form-row">
          <Input label="Budget Min" type="number" value={form.budget_min} onChange={(e) => update('budget_min', e.target.value)} required />
          <Input label="Budget Max" type="number" value={form.budget_max} onChange={(e) => update('budget_max', e.target.value)} required />
        </div>

        <div className="form-row">
          <Select label="Pricing Model" options={PRICING_MODELS} value={form.pricing_model} onChange={(e) => update('pricing_model', e.target.value)} />
          <Select label="Engagement Type" options={ENGAGEMENT_TYPES} value={form.engagement_type} onChange={(e) => update('engagement_type', e.target.value)} />
        </div>

        <div className="form-row">
          <Input label="Deadline" type="date" value={form.deadline} onChange={(e) => update('deadline', e.target.value)} required />
          <Input label="Expected Delivery" value={form.expected_delivery_time} onChange={(e) => update('expected_delivery_time', e.target.value)} placeholder="e.g. 2 weeks" />
        </div>

        <Input label="Jurisdiction" value={form.jurisdiction} onChange={(e) => update('jurisdiction', e.target.value)} placeholder="US, UK, UAE..." />
        <Input label="Accounting Standard" value={form.accounting_standard} onChange={(e) => update('accounting_standard', e.target.value)} placeholder="GAAP, IFRS..." />

        <label className="checkbox-label">
          <input type="checkbox" checked={form.nda_required} onChange={(e) => update('nda_required', e.target.checked)} />
          NDA Required
        </label>

        <Button type="submit" variant="primary" size="lg" loading={mutation.isPending}>Post Job</Button>
      </form>
    </div>
  );
}
'''

EDIT_JOB_PAGE = POST_JOB_PAGE.replace('Post a New Job', 'Edit Job').replace('clientService.createJob', 'clientService.updateJob').replace("const { id } = useParams();", "const { id } = useParams();\n  const { data: jobData } = useQuery({ queryKey: ['my-job', id], queryFn: () => clientService.getJobBids(id) });")

CLIENT_JOB_DETAIL_PAGE = '''
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
              <strong>Accountant #{bid.accountant_id}</strong>
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
'''

CLIENT_PROFILE_PAGE = '''
import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
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
  const [form, setForm] = useState({ company_name: '', company_industry: '', website: '', company_description: '' });
  const [saved, setSaved] = useState(false);

  const mutation = useMutation({
    mutationFn: (data) => profileService.updateProfile(data),
    onSuccess: () => { setSaved(true); queryClient.invalidateQueries({ queryKey: ['my-profile'] }); },
  });

  return (
    <div className="profile-page container">
      <h1>{user?.name}</h1>
      <Card padding="lg">
        <Input label="Company Name" value={form.company_name} onChange={(e) => setForm({...form, company_name: e.target.value})} />
        <Input label="Industry" value={form.company_industry} onChange={(e) => setForm({...form, company_industry: e.target.value})} />
        <Input label="Website" value={form.website} onChange={(e) => setForm({...form, website: e.target.value})} />
        <Textarea label="Description" value={form.company_description} onChange={(e) => setForm({...form, company_description: e.target.value})} rows={4} />
        <Button onClick={() => mutation.mutate(form)} loading={mutation.isPending}>Save</Button>
        {saved && <span className="saved-msg">✅ Saved</span>}
      </Card>
    </div>
  );
}
'''

# ============================================================
# ADMIN PAGES
# ============================================================

ADMIN_DASHBOARD = '''
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { Card } from '../../components/ui/Card';
import './AdminPage.css';

export default function AdminDashboard() {
  const { data } = useQuery({ queryKey: ['admin', 'stats'], queryFn: adminService.getStats });
  const stats = data || {};

  const links = [
    { to: '/admin/users', label: 'Users' },
    { to: '/admin/jobs', label: 'Jobs' },
    { to: '/admin/bids', label: 'Bids' },
    { to: '/admin/categories', label: 'Categories' },
    { to: '/admin/certifications', label: 'Certifications' },
    { to: '/admin/software-skills', label: 'Software Skills' },
    { to: '/admin/countries', label: 'Countries' },
    { to: '/admin/documents', label: 'Documents' },
    { to: '/admin/content', label: 'Content' },
    { to: '/admin/audit-logs', label: 'Audit Logs' },
  ];

  return (
    <div className="admin-page">
      <aside className="admin-sidebar">
        <Link to="/admin" className="admin-logo">Admin Panel</Link>
        <nav>
          {links.map((link) => <Link key={link.to} to={link.to}>{link.label}</Link>)}
        </nav>
      </aside>
      <main className="admin-main">
        <h1>Dashboard</h1>
        <div className="stats-grid">
          <Card padding="lg"><h3>{stats.total_users || 0}</h3><p>Total Users</p></Card>
          <Card padding="lg"><h3>{stats.total_jobs || 0}</h3><p>Total Jobs</p></Card>
          <Card padding="lg"><h3>{stats.total_bids || 0}</h3><p>Total Bids</p></Card>
        </div>
      </main>
    </div>
  );
}
'''

DATA_TABLE = '''
import { Pagination } from '../ui/Pagination';
import './AdminPage.css';

export function DataTable({ columns, data, totalPages, page, onPageChange, onEdit, onDelete }) {
  return (
    <div className="data-table-wrapper">
      <table className="data-table">
        <thead>
          <tr>{columns.map((col) => <th key={col.key}>{col.label}</th>)}</tr>
        </thead>
        <tbody>
          {data?.map((row, i) => (
            <tr key={row.id || i}>
              {columns.map((col) => (
                <td key={col.key}>{col.render ? col.render(row) : row[col.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {totalPages > 1 && <Pagination page={page} totalPages={totalPages} onPageChange={onPageChange} />}
    </div>
  );
}
'''

USERS_PAGE = '''
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import './AdminPage.css';

export default function UsersPage() {
  const [page, setPage] = useState(1);
  const { data } = useQuery({ queryKey: ['admin', 'users', page], queryFn: () => adminService.list('users', { page }) });

  const columns = [
    { key: 'name', label: 'Name' },
    { key: 'email', label: 'Email' },
    { key: 'role', label: 'Role', render: (r) => <Badge variant={r.role === 'admin' ? 'primary' : 'neutral'}>{r.role}</Badge> },
    { key: 'is_active', label: 'Active', render: (r) => r.is_active ? '✅' : '❌' },
  ];

  return (
    <div className="admin-page">
      <aside className="admin-sidebar"><nav>{/* same sidebar links */}</nav></aside>
      <main className="admin-main">
        <h1>Users</h1>
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />
      </main>
    </div>
  );
}
'''

ADMIN_JOBS_PAGE = USERS_PAGE.replace("'users'", "'jobs'").replace("Users", "Jobs").replace("name", "title").replace("email", "status").replace("role", "bids_count").replace("is_active", "deadline")
ADMIN_BIDS_PAGE = USERS_PAGE.replace("'users'", "'bids'").replace("Users", "Bids").replace("name", "price").replace("email", "job_id").replace("role", "status").replace("is_active", "created_at")
ADMIN_CATEGORIES_PAGE = USERS_PAGE.replace("'users'", "'categories'").replace("Users", "Categories").replace("name", "name").replace("email", "slug").replace("role", "parent_id").replace("is_active", "sort_order")
ADMIN_CERTIFICATIONS_PAGE = USERS_PAGE.replace("'users'", "'certifications'").replace("Users", "Certifications").replace("name", "name").replace("email", "issuing_body").replace("role", "region").replace("is_active", "is_active")
ADMIN_SOFTWARE_PAGE = USERS_PAGE.replace("'users'", "'software-skills'").replace("Users", "Software Skills").replace("name", "name").replace("email", "is_active").replace("role", "created_at").replace("is_active", "")
ADMIN_COUNTRIES_PAGE = USERS_PAGE.replace("'users'", "'countries'").replace("Users", "Countries").replace("name", "country_name_en").replace("email", "currency_iso_code").replace("role", "phone_code").replace("is_active", "is_active")
ADMIN_DOCUMENTS_PAGE = USERS_PAGE.replace("'users'", "'documents'").replace("Users", "Documents").replace("name", "document_type").replace("email", "file_name").replace("role", "is_verified").replace("is_active", "uploaded_at")
ADMIN_CONTENT_PAGE = USERS_PAGE.replace("'users'", "'content'").replace("Users", "Content").replace("name", "key").replace("email", "title").replace("role", "version").replace("is_active", "is_active")

AUDIT_LOGS_PAGE_EXTRA = '''
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '../../services/adminService';
import { DataTable } from './DataTable';
import { Badge } from '../../components/ui/Badge';
import { SearchBar } from '../../components/ui/SearchBar';
import { formatFullDate } from '../../utils/formatDate';
import './AdminPage.css';

export default function AuditLogsPage() {
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({});

  const { data } = useQuery({
    queryKey: ['admin', 'audit-logs', page, filters],
    queryFn: () => adminService.getAuditLogs({ ...filters, page }),
  });

  const columns = [
    { key: 'action', label: 'Action' },
    { key: 'user_email', label: 'User' },
    { key: 'action_category', label: 'Category' },
    { key: 'entity_type', label: 'Entity' },
    { key: 'description', label: 'Description', render: (r) => r.description?.substring(0, 80) || '—' },
    { key: 'created_at', label: 'Date', render: (r) => formatFullDate(r.created_at) },
  ];

  return (
    <div className="admin-page">
      <aside className="admin-sidebar"><nav></nav></aside>
      <main className="admin-main">
        <h1>Audit Logs</h1>
        <div className="audit-filters">
          <select onChange={(e) => setFilters({...filters, action_category: e.target.value})}>
            <option value="">All Categories</option>
            <option value="authentication">Authentication</option>
            <option value="job">Job</option>
            <option value="bid">Bid</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <DataTable columns={columns} data={data?.data} totalPages={data?.meta?.last_page} page={page} onPageChange={setPage} />
      </main>
    </div>
  );
}
'''

ADMIN_AUDIT_LOGS_PAGE = AUDIT_LOGS_PAGE_EXTRA

APP_JSX_FULL = '''
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import { Layout } from './components/layout/Layout';
import { ProtectedRoute } from './components/layout/ProtectedRoute';

import JobListPage from './pages/public/JobListPage';
import JobDetailPage from './pages/public/JobDetailPage';
import LoginPage from './pages/public/LoginPage';
import RegisterPage from './pages/public/RegisterPage';

import AccountantDashboard from './pages/accountant/AccountantDashboard';
import MyBidsPage from './pages/accountant/MyBidsPage';
import AccountantProfilePage from './pages/accountant/AccountantProfilePage';

import ClientDashboard from './pages/client/ClientDashboard';
import PostJobPage from './pages/client/PostJobPage';
import EditJobPage from './pages/client/EditJobPage';
import ClientJobDetailPage from './pages/client/ClientJobDetailPage';
import ClientProfilePage from './pages/client/ClientProfilePage';

import AdminDashboard from './pages/admin/AdminDashboard';
import UsersPage from './pages/admin/UsersPage';
import JobsPage from './pages/admin/JobsPage';
import BidsPage from './pages/admin/BidsPage';
import CategoriesPage from './pages/admin/CategoriesPage';
import CertificationsPage from './pages/admin/CertificationsPage';
import SoftwareSkillsPage from './pages/admin/SoftwareSkillsPage';
import CountriesPage from './pages/admin/CountriesPage';
import DocumentsPage from './pages/admin/DocumentsPage';
import ContentPage from './pages/admin/ContentPage';
import AuditLogsPage from './pages/admin/AuditLogsPage';

export default function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <Routes>
          <Route path="/" element={<Layout />}>
            {/* Public */}
            <Route index element={<JobListPage />} />
            <Route path="jobs/:id" element={<JobDetailPage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="register" element={<RegisterPage />} />

            {/* Accountant */}
            <Route element={<ProtectedRoute role="accountant" />}>
              <Route path="dashboard" element={<AccountantDashboard />} />
              <Route path="my-bids" element={<MyBidsPage />} />
              <Route path="profile" element={<AccountantProfilePage />} />
            </Route>

            {/* Client */}
            <Route element={<ProtectedRoute role="client" />}>
              <Route path="client/dashboard" element={<ClientDashboard />} />
              <Route path="client/jobs/new" element={<PostJobPage />} />
              <Route path="client/jobs/:id/edit" element={<EditJobPage />} />
              <Route path="client/jobs/:id" element={<ClientJobDetailPage />} />
              <Route path="client/profile" element={<ClientProfilePage />} />
            </Route>

            {/* Admin */}
            <Route element={<ProtectedRoute role="admin" />}>
              <Route path="admin" element={<AdminDashboard />} />
              <Route path="admin/users" element={<UsersPage />} />
              <Route path="admin/jobs" element={<JobsPage />} />
              <Route path="admin/bids" element={<BidsPage />} />
              <Route path="admin/categories" element={<CategoriesPage />} />
              <Route path="admin/certifications" element={<CertificationsPage />} />
              <Route path="admin/software-skills" element={<SoftwareSkillsPage />} />
              <Route path="admin/countries" element={<CountriesPage />} />
              <Route path="admin/documents" element={<DocumentsPage />} />
              <Route path="admin/content" element={<ContentPage />} />
              <Route path="admin/audit-logs" element={<AuditLogsPage />} />
            </Route>
          </Route>
        </Routes>
      </ToastProvider>
    </AuthProvider>
  );
}
'''

# ============================================================
# CSS FILES
# ============================================================

BUTTON_CSS = '''
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; border-radius: var(--radius-md); font-weight: 500; transition: all 0.2s; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary { background: var(--color-primary); color: #fff; }
.btn-primary:hover:not(:disabled) { background: var(--color-primary-dark); }
.btn-outline { background: transparent; border: 1px solid var(--color-primary); color: var(--color-primary); }
.btn-ghost { background: transparent; color: var(--color-text-secondary); }
.btn-ghost:hover { background: var(--color-bg-hover); }
.btn-danger { background: var(--color-danger); color: #fff; }
.btn-sm { padding: 6px 12px; font-size: 12px; }
.btn-md { padding: 8px 16px; font-size: 13px; }
.btn-lg { padding: 12px 24px; font-size: 14px; }
.btn-full { width: 100%; }
.btn-text-hidden { visibility: hidden; position: absolute; }
'''

INPUT_CSS = '''
.input-group { margin-bottom: 16px; }
.input-label { display: block; font-size: 13px; font-weight: 500; color: var(--color-text-primary); margin-bottom: 6px; }
.required { color: var(--color-danger); margin-left: 2px; }
.input-wrapper { position: relative; display: flex; align-items: center; }
.input-field { width: 100%; padding: 10px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-md); background: var(--color-bg-surface); color: var(--color-text-primary); font-size: 14px; transition: border-color 0.2s, box-shadow 0.2s; }
.input-field:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(1,154,81,0.12); }
.input-error .input-field { border-color: var(--color-danger); }
.input-error-text { font-size: 12px; color: var(--color-danger); margin-top: 4px; display: block; }
.input-hint { font-size: 12px; color: var(--color-text-muted); margin-top: 4px; display: block; }
.input-prefix, .input-suffix { padding: 0 10px; color: var(--color-text-muted); font-size: 13px; }
.select-field { appearance: none; padding-right: 32px; }
.select-chevron { position: absolute; right: 10px; color: var(--color-text-muted); pointer-events: none; font-size: 10px; }
.textarea-field { resize: vertical; min-height: 80px; }
.textarea-footer { display: flex; justify-content: space-between; }
.char-count { font-size: 11px; color: var(--color-text-muted); }
.checkbox-label { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--color-text-secondary); cursor: pointer; margin-bottom: 8px; }
'''

BADGE_CSS = '''
.badge { display: inline-block; padding: 2px 8px; border-radius: var(--radius-full); font-size: 11px; font-weight: 600; }
.badge-success { background: var(--color-status-open-bg); color: var(--color-status-open-text); }
.badge-danger { background: var(--color-status-closed-bg); color: var(--color-status-closed-text); }
.badge-warning { background: var(--color-warning-light); color: var(--color-warning); }
.badge-neutral { background: var(--color-bg-hover); color: var(--color-text-secondary); }
.badge-primary { background: var(--color-primary-light); color: var(--color-primary-text); }
'''

CARD_CSS = '''
.card { background: var(--color-bg-surface); border: 1px solid var(--color-border); border-radius: var(--radius-lg); transition: border-color 0.2s, box-shadow 0.2s; }
.card-hoverable:hover { border-color: var(--color-primary); box-shadow: var(--shadow-md); cursor: pointer; }
.card-padding-sm { padding: 12px; }
.card-padding-md { padding: 16px; }
.card-padding-lg { padding: 24px; }
'''

MODAL_CSS = '''
.modal-overlay { position: fixed; inset: 0; background: var(--color-backdrop); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: var(--color-bg-surface); border-radius: var(--radius-xl); max-height: 85vh; overflow-y: auto; }
.modal-sm { width: 400px; }
.modal-md { width: 560px; }
.modal-lg { width: 720px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 24px 0; }
.modal-header h2 { font-size: 18px; }
.modal-close { background: none; font-size: 20px; color: var(--color-text-muted); }
.modal-body { padding: 20px 24px; }
'''

SKELETON_CSS = '''
.skeleton { background: linear-gradient(90deg, var(--color-skeleton) 25%, var(--color-skeleton-shine) 50%, var(--color-skeleton) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: var(--radius-md); }
.skeleton-text { height: 14px; border-radius: 4px; }
.skeleton-rect { height: 100%; }
.skeleton-circle { border-radius: 50%; }
'''

PAGINATION_CSS = '''
.pagination { display: flex; align-items: center; justify-content: center; gap: 4px; margin-top: 32px; }
.pagination-btn { width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: var(--radius-md); background: var(--color-bg-surface); border: 1px solid var(--color-border); color: var(--color-text-secondary); font-size: 13px; cursor: pointer; }
.pagination-btn:hover:not(:disabled) { border-color: var(--color-primary); }
.pagination-btn.active { background: var(--color-primary); color: #fff; border-color: var(--color-primary); }
.pagination-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.pagination-ellipsis { padding: 0 4px; color: var(--color-text-muted); }
'''

SEARCHBAR_CSS = '''
.search-bar { position: relative; display: flex; align-items: center; max-width: 500px; margin: 0 auto; }
.search-icon { position: absolute; left: 14px; font-size: 16px; }
.search-input { width: 100%; padding: 12px 40px 12px 42px; border: 1px solid var(--color-border); border-radius: var(--radius-full); background: var(--color-bg-surface); font-size: 14px; color: var(--color-text-primary); }
.search-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(1,154,81,0.1); }
.search-clear { position: absolute; right: 12px; background: none; color: var(--color-text-muted); font-size: 14px; }
'''

EMPTYSTATE_CSS = '''
.empty-state { text-align: center; padding: 64px 24px; }
.empty-state-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state-title { font-size: 18px; color: var(--color-text-primary); margin-bottom: 8px; }
.empty-state-description { color: var(--color-text-muted); margin-bottom: 24px; }
'''

TOAST_CSS = '''
.toast-container { position: fixed; bottom: 24px; right: 24px; z-index: 2000; display: flex; flex-direction: column; gap: 8px; }
.toast { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border-radius: var(--radius-md); background: var(--color-bg-surface); border: 1px solid var(--color-border); box-shadow: var(--shadow-lg); min-width: 300px; }
.toast-success { border-left: 4px solid var(--color-primary); }
.toast-error { border-left: 4px solid var(--color-danger); }
.toast-info { border-left: 4px solid var(--color-warning); }
.toast-message { flex: 1; font-size: 13px; color: var(--color-text-primary); }
.toast-close { background: none; color: var(--color-text-muted); font-size: 14px; }
'''

SPINNER_CSS = '''
.spinner { border: 3px solid var(--color-border); border-top-color: var(--color-primary); border-radius: 50%; animation: spin 0.6s linear infinite; }
.spinner-sm { width: 16px; height: 16px; }
.spinner-md { width: 24px; height: 24px; }
.spinner-lg { width: 36px; height: 36px; }
'''

MULTISELECT_CSS = '''
.multiselect { position: relative; }
.multiselect-trigger { display: flex; align-items: center; justify-content: space-between; min-height: 42px; padding: 8px 12px; border: 1px solid var(--color-border); border-radius: var(--radius-md); cursor: pointer; }
.multiselect-chips { display: flex; flex-wrap: wrap; gap: 4px; }
.multiselect-chip { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; background: var(--color-primary-light); color: var(--color-primary-text); border-radius: var(--radius-full); font-size: 12px; }
.multiselect-chip button { background: none; color: inherit; font-size: 10px; }
.multiselect-placeholder { color: var(--color-text-placeholder); font-size: 14px; }
.multiselect-dropdown { position: absolute; top: 100%; left: 0; right: 0; background: var(--color-bg-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); z-index: 100; margin-top: 4px; max-height: 250px; overflow-y: auto; }
.multiselect-search { width: 100%; padding: 8px 12px; border: none; border-bottom: 1px solid var(--color-border); font-size: 13px; }
.multiselect-option { display: flex; align-items: center; gap: 8px; padding: 8px 12px; font-size: 13px; cursor: pointer; }
.multiselect-option:hover { background: var(--color-bg-hover); }
.multiselect-no-results { padding: 12px; color: var(--color-text-muted); font-size: 13px; }
'''

DISCLAIMER_CSS = '''
.disclaimer-banner { padding: 24px; border: 2px solid var(--color-warning); border-radius: var(--radius-lg); background: var(--color-warning-light); margin: 24px 0; }
.disclaimer-content h3 { margin-bottom: 12px; }
.disclaimer-text { font-size: 13px; color: var(--color-text-secondary); margin-bottom: 16px; white-space: pre-line; }
.disclaimer-actions { display: flex; gap: 12px; }
'''

NAVBAR_CSS = '''
.navbar { position: sticky; top: 0; z-index: 500; background: var(--color-bg-surface); border-bottom: 1px solid var(--color-border); }
.navbar-inner { max-width: 1280px; margin: 0 auto; padding: 0 24px; height: 60px; display: flex; align-items: center; justify-content: space-between; }
.navbar-logo { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 600; color: var(--color-text-primary); }
.logo-green { color: var(--color-primary); }
.navbar-links { display: flex; gap: 24px; align-items: center; }
.navbar-links a { font-size: 13px; color: var(--color-text-secondary); }
.navbar-links a:hover { color: var(--color-primary); }
.navbar-actions { display: flex; align-items: center; gap: 8px; }
.nav-icon-btn { background: none; font-size: 16px; padding: 6px; border-radius: var(--radius-md); color: var(--color-text-secondary); }
.nav-icon-btn:hover { background: var(--color-bg-hover); }
.navbar-user { display: flex; align-items: center; gap: 12px; }
.nav-user-link { display: flex; align-items: center; gap: 6px; color: var(--color-text-secondary); font-size: 13px; }
.nav-avatar { font-size: 18px; }
.hamburger { display: none; background: none; font-size: 22px; padding: 6px; }
@media (max-width: 768px) {
  .navbar-links { display: none; position: absolute; top: 60px; left: 0; right: 0; background: var(--color-bg-surface); flex-direction: column; padding: 16px; border-bottom: 1px solid var(--color-border); }
  .navbar-links.open { display: flex; }
  .hamburger { display: block; }
  .navbar-auth { display: none; }
}
'''

FOOTER_CSS = '''
.footer { border-top: 1px solid var(--color-border); margin-top: 64px; padding: 32px 0; }
.footer-inner { max-width: 1280px; margin: 0 auto; padding: 0 24px; display: flex; justify-content: space-between; }
.footer-logo { font-family: 'Playfair Display', serif; font-size: 18px; color: var(--color-text-primary); }
.footer-disclaimer { font-size: 12px; color: var(--color-text-muted); max-width: 400px; margin-top: 8px; }
.footer-links { display: flex; gap: 24px; align-items: center; }
.footer-links a { font-size: 13px; color: var(--color-text-muted); }
@media (max-width: 768px) { .footer-inner { flex-direction: column; gap: 16px; } }
'''

SIDEBAR_CSS = '''
.sidebar { width: 240px; flex-shrink: 0; }
.sidebar-body { display: flex; flex-direction: column; gap: 16px; }
.sidebar-header { display: none; }
.sidebar-close { display: none; }
.filter-group { display: flex; flex-direction: column; gap: 4px; }
.filter-label { font-size: 12px; font-weight: 600; color: var(--color-text-primary); text-transform: uppercase; letter-spacing: 0.5px; }
.filter-range { display: flex; gap: 8px; align-items: center; }
.filter-range input { width: 80px; }
.sidebar-footer { margin-top: 16px; }
@media (max-width: 1023px) {
  .sidebar { position: fixed; left: -280px; top: 0; bottom: 0; width: 280px; background: var(--color-bg-surface); z-index: 900; transition: left 0.3s; padding: 20px; overflow-y: auto; }
  .sidebar-open { left: 0; }
  .sidebar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
  .sidebar-close { display: block; background: none; font-size: 20px; }
  .sidebar-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 899; }
}
'''

LAYOUT_CSS = '''
.layout { min-height: 100vh; display: flex; flex-direction: column; }
.main-content { flex: 1; }
.loading-screen { display: flex; align-items: center; justify-content: center; height: 100vh; font-size: 18px; color: var(--color-text-muted); }
'''

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    print("="*60)
    print("ACCOUNTANT HUB - FRONTEND SETUP PHASE II")
    print("="*60)
    os.chdir(BASE_DIR)

    create_public_pages()
    create_job_components()
    create_accountant_pages()
    create_client_pages()
    create_admin_pages()
    update_app_routing()
    add_component_css()

    print_summary()