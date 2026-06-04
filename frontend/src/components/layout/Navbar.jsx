
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useTheme } from '../../hooks/useTheme';
import { useLanguage } from '../../hooks/useLanguage';
import { Button } from '../ui/Button';
import './Navbar.css';

export function Navbar() {
  const { t } = useTranslation();
  const { isAuthenticated, role, user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-logo">
          Accountant<span className="logo-green">Hub</span>
        </Link>

        <div className={`navbar-links ${menuOpen ? 'open' : ''}`}>
          <Link to="/" onClick={() => setMenuOpen(false)}>{t('nav.browseJobs')}</Link>

          {isAuthenticated && role === 'accountant' && (
            <>
              <Link to="/dashboard" onClick={() => setMenuOpen(false)}>{t('nav.dashboard')}</Link>
              <Link to="/my-bids" onClick={() => setMenuOpen(false)}>{t('nav.myBids')}</Link>
            </>
          )}

          {isAuthenticated && role === 'client' && (
            <>
              <Link to="/client/dashboard" onClick={() => setMenuOpen(false)}>{t('nav.dashboard')}</Link>
              <Link to="/client/jobs/new" onClick={() => setMenuOpen(false)}>{t('nav.postJob')}</Link>
            </>
          )}

          {isAuthenticated && role === 'admin' && (
            <Link to="/admin" onClick={() => setMenuOpen(false)}>{t('nav.admin')}</Link>
          )}
        </div>

        <div className="navbar-actions">
          <button className="nav-icon-btn" onClick={toggleTheme} title={t(`theme.${theme}`)}>
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
          <button className="nav-icon-btn" onClick={toggleLanguage} title={t(`language.${language}`)}>
            {language === 'en' ? 'AR' : 'EN'}
          </button>

          {isAuthenticated ? (
            <div className="navbar-user">
              <Link to={role === 'client' ? '/client/profile' : '/profile'} className="nav-user-link">
                <span className="nav-avatar">👤</span>
                <span className="nav-username">{user?.name}</span>
              </Link>
              <Button variant="ghost" size="sm" onClick={handleLogout}>{t('nav.logout')}</Button>
            </div>
          ) : (
            <div className="navbar-auth">
              <Link to="/login"><Button variant="ghost" size="sm">{t('nav.login')}</Button></Link>
              <Link to="/register"><Button variant="primary" size="sm">{t('nav.register')}</Button></Link>
            </div>
          )}

          <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>
    </nav>
  );
}
