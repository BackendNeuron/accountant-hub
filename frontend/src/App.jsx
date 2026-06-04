
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
import AccountantProfileView from './pages/client/AccountantProfileView';
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
import TermsPage from './pages/public/TermsPage';
import PrivacyPage from './pages/public/PrivacyPage';

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
            <Route path="terms" element={<TermsPage />} />
            <Route path="privacy" element={<PrivacyPage />} />

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
              <Route path="accountant/:id" element={<AccountantProfileView />} />
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
