import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../../hooks/useAuth';
import { jobService } from '../../services/jobService';
import { Input } from '../../components/ui/Input';
import { Select } from '../../components/ui/Select';
import { Button } from '../../components/ui/Button';
import './AuthPage.css';

export default function RegisterPage() {
  const { t } = useTranslation();
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [role, setRole] = useState('accountant');
  const [form, setForm] = useState({
    name: '', email: '', phone: '', password: '',
    company_name: '', country_code: '', phone_digits_count: 0,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [phoneError, setPhoneError] = useState('');

  const { data: countriesData } = useQuery({
    queryKey: ['countries'],
    queryFn: jobService.getCountries,
  });

  const countries = countriesData || [];
  const countryOptions = countries.map((c) => ({
    value: c.country_iso_code2,
    label: `${c.country_name_en} (${c.phone_code})`,
  }));

  const handleCountryChange = (code) => {
    const country = countries.find((c) => c.country_iso_code2 === code);
    setForm({
      ...form,
      country_code: code,
      phone_digits_count: country?.phone_digits_count || 0,
    });
    setPhoneError('');
  };

  const validatePhone = (phone) => {
    if (!form.country_code) {
      setPhoneError('Please select a country first');
      return false;
    }
    const digits = phone.replace(/\D/g, '');
    if (form.phone_digits_count && digits.length !== form.phone_digits_count) {
      setPhoneError(`Phone must be exactly ${form.phone_digits_count} digits for the selected country`);
      return false;
    }
    if (digits.length < 7) {
      setPhoneError('Phone number is too short');
      return false;
    }
    setPhoneError('');
    return true;
  };

  const validatePassword = (password) => {
    if (password.length < 8) return 'Password must be at least 8 characters';
    if (!/[A-Z]/.test(password)) return 'Password must contain an uppercase letter';
    if (!/[a-z]/.test(password)) return 'Password must contain a lowercase letter';
    if (!/[0-9]/.test(password)) return 'Password must contain a number';
    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!validatePhone(form.phone)) return;

    const passwordError = validatePassword(form.password);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setLoading(true);
    try {
      const data = {
        name: form.name,
        email: form.email,
        phone: form.phone,
        password: form.password,
        role,
      };
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
          <button className={`role-btn ${role === 'accountant' ? 'active' : ''}`} onClick={() => setRole('accountant')}>
            {t('auth.accountantRole')}
          </button>
          <button className={`role-btn ${role === 'client' ? 'active' : ''}`} onClick={() => setRole('client')}>
            {t('auth.clientRole')}
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {error && <div className="auth-error">{error}</div>}

          <Input
            label={t('auth.fullName')}
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
          <Input
            label={t('auth.email')}
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />

          <Select
            label="Country"
            options={countryOptions}
            value={form.country_code}
            onChange={(e) => handleCountryChange(e.target.value)}
            placeholder="Select your country..."
            required
          />

          <Input
            label={t('auth.phone')}
            type="tel"
            value={form.phone}
            onChange={(e) => {
              setForm({ ...form, phone: e.target.value });
              if (form.country_code) validatePhone(e.target.value);
            }}
            error={phoneError}
            hint={form.phone_digits_count ? `Expected ${form.phone_digits_count} digits` : ''}
            required
          />

          {role === 'client' && (
            <Input
              label={t('auth.companyName')}
              value={form.company_name}
              onChange={(e) => setForm({ ...form, company_name: e.target.value })}
              required
            />
          )}

          <Input
            label={t('auth.password')}
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
            minLength={8}
            hint="Min 8 chars, uppercase, lowercase, number"
          />

          <Button type="submit" variant="primary" size="lg" loading={loading} className="btn-full">
            {t('auth.registerBtn')}
          </Button>
        </form>
        <p className="auth-footer">
          {t('auth.haveAccount')} <Link to="/login">{t('auth.loginLink')}</Link>
        </p>
      </div>
    </div>
  );
}