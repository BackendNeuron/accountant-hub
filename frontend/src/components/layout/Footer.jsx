import { Link } from 'react-router-dom';
import './Footer.css';

export function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">
          <span className="footer-logo">Accountant<span className="logo-green">Hub</span></span>
          <p className="footer-disclaimer">
            Accountant Hub is a marketplace connecting businesses with independent accounting professionals.
            We do not employ or guarantee the work of any professional.
          </p>
        </div>
        <div className="footer-links">
          <Link to="/">Browse Jobs</Link>
          <Link to="/terms">Terms of Service</Link>
          <Link to="/privacy">Privacy Policy</Link>
        </div>
      </div>
    </footer>
  );
}
