
import './Input.css';

export function Textarea({
  label,
  placeholder,
  value,
  onChange,
  error,
  rows = 4,
  maxLength,
  name,
  required,
}) {
  return (
    <div className={`input-group ${error ? 'input-error' : ''}`}>
      {label && <label className="input-label" htmlFor={name}>{label}{required && <span className="required">*</span>}</label>}
      <textarea
        id={name}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        rows={rows}
        maxLength={maxLength}
        className="input-field textarea-field"
        required={required}
      />
      <div className="textarea-footer">
        {error && <span className="input-error-text">{error}</span>}
        {maxLength && (
          <span className="char-count">{value?.length || 0}/{maxLength}</span>
        )}
      </div>
    </div>
  );
}
