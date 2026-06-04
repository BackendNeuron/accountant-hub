
import { Button } from './Button';
import './DisclaimerBanner.css';

export function DisclaimerBanner({ title, text, onAccept, onDecline, acceptLabel = 'Accept', declineLabel = 'Decline' }) {
  return (
    <div className="disclaimer-banner animate-fade-in">
      <div className="disclaimer-content">
        <h3>{title}</h3>
        <div className="disclaimer-text">{text}</div>
        <div className="disclaimer-actions">
          <Button variant="primary" onClick={onAccept}>{acceptLabel}</Button>
          {onDecline && <Button variant="ghost" onClick={onDecline}>{declineLabel}</Button>}
        </div>
      </div>
    </div>
  );
}
