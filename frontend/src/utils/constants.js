
export const ROLES = {
  ADMIN: 'admin',
  CLIENT: 'client',
  ACCOUNTANT: 'accountant',
};

export const JOB_STATUS = {
  OPEN: 'open',
  CLOSED: 'closed',
};

export const BID_STATUS = {
  PENDING: 'pending',
  ACCEPTED: 'accepted',
  REJECTED: 'rejected',
};

export const PRICING_MODELS = [
  { value: 'fixed', label: 'Fixed Price' },
  { value: 'hourly', label: 'Hourly' },
  { value: 'retainer', label: 'Retainer' },
];

export const ENGAGEMENT_TYPES = [
  { value: 'one_time', label: 'One-Time' },
  { value: 'recurring', label: 'Recurring' },
];

export const SORT_OPTIONS = [
  { value: 'newest', label: 'Newest' },
  { value: 'budget_high', label: 'Highest Budget' },
  { value: 'budget_low', label: 'Lowest Budget' },
  { value: 'bids', label: 'Most Bids' },
  { value: 'deadline', label: 'Deadline' },
];
