
import './Input.css';

export function Input({
  label,
  placeholder,
  value,
  onChange,
  error,
  hint,
  disabled,
  prefix,
  suffix,
  type = 'text',
  name,
  required,
  ...props
}) {
  return (
    <div className={`input-group ${error ? 'input-error' : ''}`}>
      {label && <label className="input-label" htmlFor={name}>{label}{required && <span className="required">*</span>}</label>}
      <div className="input-wrapper">
        {prefix && <span className="input-prefix">{prefix}</span>}
        <input
          id={name}
          name={name}
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          disabled={disabled}
          className="input-field"
          required={required}
          {...props}
        />
        {suffix && <span className="input-suffix">{suffix}</span>}
      </div>
      {error && <span className="input-error-text">{error}</span>}
      {hint && !error && <span className="input-hint">{hint}</span>}
    </div>
  );
}
