
import './Spinner.css';

export function Spinner({ size = 'md', color }) {
  return (
    <div
      className={`spinner spinner-${size}`}
      style={color ? { borderTopColor: color } : undefined}
    />
  );
}
