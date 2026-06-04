import { useState, useRef, useEffect } from 'react';
import './MultiSelect.css';

export function MultiSelect({ label, options = [], selected = [], onChange, placeholder = 'Select...' }) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setIsOpen(false);
        setSearch('');
      }
    };
    document.addEventListener('click', handler);
    return () => document.removeEventListener('click', handler);
  }, []);

  const filtered = options.filter((opt) =>
    opt.label.toLowerCase().includes(search.toLowerCase())
  );

  const handleToggle = (value, e) => {
    e.stopPropagation();
    const next = selected.includes(value)
      ? selected.filter((v) => v !== value)
      : [...selected, value];
    onChange(next);
  };

  const handleRemove = (value, e) => {
    e.stopPropagation();
    onChange(selected.filter((v) => v !== value));
  };

  const handleTrigger = (e) => {
    e.stopPropagation();
    setIsOpen(!isOpen);
  };

  return (
    <div className="multiselect" ref={ref}>
      {label && <label className="input-label">{label}</label>}
      <div className="multiselect-trigger" onClick={handleTrigger}>
        <div className="multiselect-chips">
          {selected.length === 0 && (
            <span className="multiselect-placeholder">{placeholder}</span>
          )}
          {selected.map((val) => {
            const opt = options.find((o) => o.value === val);
            return (
              <span key={val} className="multiselect-chip">
                {opt?.label || val}
                <button type="button" onClick={(e) => handleRemove(val, e)}>x</button>
              </span>
            );
          })}
        </div>
        <span className="chevron">{isOpen ? '^' : 'v'}</span>
      </div>
      {isOpen && (
        <div className="multiselect-dropdown" onClick={(e) => e.stopPropagation()}>
          <input
            type="text"
            className="multiselect-search"
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onClick={(e) => e.stopPropagation()}
            autoFocus
          />
          <div className="multiselect-options">
            {filtered.length === 0 && (
              <div className="multiselect-no-results">No results</div>
            )}
            {filtered.map((opt) => {
              const isChecked = selected.includes(opt.value);
              return (
                <div
                  key={opt.value}
                  className={`multiselect-option ${isChecked ? 'checked' : ''}`}
                  onClick={(e) => handleToggle(opt.value, e)}
                >
                  <span className={`check-box ${isChecked ? 'ticked' : ''}`}>
                    {isChecked && 'x'}
                  </span>
                  <span>{opt.label}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}