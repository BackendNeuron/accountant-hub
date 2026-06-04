
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
