
import { formatDistanceToNow, format, isToday, isYesterday } from 'date-fns';

export function formatRelativeDate(dateString) {
  const date = new Date(dateString);
  if (isToday(date)) return 'Today';
  if (isYesterday(date)) return 'Yesterday';
  return formatDistanceToNow(date, { addSuffix: true });
}

export function formatDeadline(dateString) {
  const date = new Date(dateString);
  return format(date, 'MMM dd, yyyy');
}

export function formatFullDate(dateString) {
  const date = new Date(dateString);
  return format(date, 'MMMM dd, yyyy');
}
