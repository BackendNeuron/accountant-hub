
import './Skeleton.css';

export function Skeleton({ width, height, variant = 'text' }) {
  return (
    <div
      className={`skeleton skeleton-${variant}`}
      style={{ width: width || '100%', height: height || '16px' }}
    />
  );
}
