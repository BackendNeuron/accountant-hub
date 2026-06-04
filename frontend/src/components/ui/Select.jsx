
import './Input.css';

export function Select({
  label,
  options = [],
  value,
  onChange,
  error,
  placeholder = 'Select...',
  name,
  required,
}) {
  return (
    <div className={`input-group ${error ? 'input-error' : ''}`}>
      {label && <label className="input-label" htmlFor={name}>{label}{required && <span className="required">*</span>}</label>}
      <div className="input-wrapper">
        <select
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          className="input-field select-field"
          required={required}
        >
          <option value="">{placeholder}</option>
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
        <span className="select-chevron">▾</span>
      </div>
      {error && <span className="input-error-text">{error}</span>}
    </div>
  );
}
