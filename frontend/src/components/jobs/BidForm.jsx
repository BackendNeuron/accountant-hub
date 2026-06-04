
import { useState, useContext } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { bidService } from '../../services/bidService';
import { ToastContext } from '../../context/ToastContext';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { Textarea } from '../ui/Textarea';
import { Button } from '../ui/Button';
import { PRICING_MODELS } from '../../utils/constants';
import './BidForm.css';

export function BidForm({ jobId, jobCurrency = 'USD', onSuccess }) {
  const { t } = useTranslation();
  const { toast } = useContext(ToastContext);
  const queryClient = useQueryClient();
  const [errors, setErrors] = useState({});

  const [form, setForm] = useState({
    price: '',
    pricing_model: 'fixed',
    delivery_time: '',
    estimated_hours: '',
    proposal_letter: '',
    engagement_terms: '',
    services_included: ['Accounting Services'],
    includes_all_fees: true,
    jurisdiction_confirmed: false,
    terms_accepted: false,
  });

  const mutation = useMutation({
    mutationFn: (data) => bidService.submitBid(jobId, data),
    onSuccess: () => {
      toast.success(t('bidForm.success'));
      queryClient.invalidateQueries({ queryKey: ['job', String(jobId)] });
      queryClient.invalidateQueries({ queryKey: ['my-bids'] });
      onSuccess();
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || t('bidForm.error'));
    },
  });

  const validate = () => {
    const errs = {};
    if (!form.price || parseFloat(form.price) <= 0) errs.price = 'Required';
    if (!form.delivery_time) errs.delivery_time = 'Required';
    if (!form.proposal_letter || form.proposal_letter.length < 50) errs.proposal_letter = 'Min 50 characters';
    if (!form.jurisdiction_confirmed) errs.jurisdiction_confirmed = 'Required';
    if (!form.terms_accepted) errs.terms_accepted = 'Required';
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    mutation.mutate({
      ...form,
      price: parseFloat(form.price),
      estimated_hours: form.estimated_hours ? parseInt(form.estimated_hours) : null,
    });
  };

  const update = (key, value) => setForm((prev) => ({ ...prev, [key]: value }));

  return (
    <form className="bid-form" onSubmit={handleSubmit}>
      <Input label={t('bidForm.price')} type="number" prefix={jobCurrency} value={form.price} onChange={(e) => update('price', e.target.value)} error={errors.price} required />
      <Select label={t('bidForm.pricingModel')} options={PRICING_MODELS} value={form.pricing_model} onChange={(e) => update('pricing_model', e.target.value)} />
      <Input label={t('bidForm.deliveryTime')} value={form.delivery_time} onChange={(e) => update('delivery_time', e.target.value)} error={errors.delivery_time} placeholder="e.g. 2 weeks" required />
      <Input label={t('bidForm.estimatedHours')} type="number" value={form.estimated_hours} onChange={(e) => update('estimated_hours', e.target.value)} />
      <Textarea label={t('bidForm.coverLetter')} value={form.proposal_letter} onChange={(e) => update('proposal_letter', e.target.value)} rows={5} maxLength={2000} error={errors.proposal_letter} required />
      <Textarea label={t('bidForm.experience')} value={form.engagement_terms} onChange={(e) => update('engagement_terms', e.target.value)} rows={3} />

      <label className="checkbox-label">
        <input type="checkbox" checked={form.includes_all_fees} onChange={(e) => update('includes_all_fees', e.target.checked)} />
        {t('bidForm.allFeesIncluded')}
      </label>
      <label className="checkbox-label">
        <input type="checkbox" checked={form.jurisdiction_confirmed} onChange={(e) => update('jurisdiction_confirmed', e.target.checked)} />
        {t('bidForm.jurisdictionConfirm')}
        {errors.jurisdiction_confirmed && <span className="input-error-text">{errors.jurisdiction_confirmed}</span>}
      </label>
      <label className="checkbox-label">
        <input type="checkbox" checked={form.terms_accepted} onChange={(e) => update('terms_accepted', e.target.checked)} />
        {t('bidForm.termsAccept')}
        {errors.terms_accepted && <span className="input-error-text">{errors.terms_accepted}</span>}
      </label>

      <Button type="submit" variant="primary" size="lg" loading={mutation.isPending} className="btn-full">
        {t('bidForm.submit')}
      </Button>
    </form>
  );
}
