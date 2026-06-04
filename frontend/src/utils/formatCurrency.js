
export function formatCurrency(amount, currency = 'USD') {
  if (amount == null) return '—';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatBudgetRange(min, max, currency = 'USD') {
  return `${formatCurrency(min, currency)} - ${formatCurrency(max, currency)}`;
}
