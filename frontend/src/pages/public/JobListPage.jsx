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
    status: searchParams.get('status') || '',
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
    const params = new URLSearchParams();
    if (filters.search) params.set('search', filters.search);
    if (filters.category) params.set('category', filters.category);
    if (filters.budget_min) params.set('budget_min', filters.budget_min);
    if (filters.budget_max) params.set('budget_max', filters.budget_max);
    if (filters.accounting_standard) params.set('accounting_standard', filters.accounting_standard);
    if (filters.jurisdiction) params.set('jurisdiction', filters.jurisdiction);
    if (filters.status) params.set('status', filters.status);
    if (filters.sort && filters.sort !== 'newest') params.set('sort', filters.sort);
    if (filters.page > 1) params.set('page', String(filters.page));
    setSearchParams(params, { replace: true });
  }, [filters, setSearchParams]);

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
  };

  const clearFilters = () => {
    setFilters({
      search: '', category: '', budget_min: '', budget_max: '',
      accounting_standard: '', jurisdiction: '', status: '', sort: 'newest', page: 1,
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
