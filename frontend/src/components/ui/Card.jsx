
import './Card.css';

export function Card({ children, onClick, hoverable = false, padding = 'md', className = '' }) {
  return (
    <div
      className={`card card-padding-${padding} ${hoverable ? 'card-hoverable' : ''} ${className}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      {children}
    </div>
  );
}
