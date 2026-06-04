import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { clientService } from '../../services/profileService';
import { jobService } from '../../services/jobService';
import { Input } from '../../components/ui/Input';
import { Select } from '../../components/ui/Select';
import { Textarea } from '../../components/ui/Textarea';
import { Button } from '../../components/ui/Button';
import { PRICING_MODELS, ENGAGEMENT_TYPES } from '../../utils/constants';
import './PostJobPage.css';

export default function PostJobPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [errors, setErrors] = useState({});

  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: jobService.getCategories });

  const [form, setForm] = useState({
    title: '', description: '', category_id: '', budget_min: '', budget_max: '',
    currency: 'USD', pricing_model: 'fixed', deadline: '', expected_delivery_time: '',
    engagement_type: 'one_time', jurisdiction: '', accounting_standard: '',
    nda_required: false,
  });

  const mutation = useMutation({
    mutationFn: (data) => clientService.createJob(data),
    onSuccess: (res) => {
      navigate('/client/dashboard');
    },
    onError: (err) => {
      if (err.response?.status === 422) {
        const backendErrors = err.response.data?.detail || [];
        const newErrors = {};
        backendErrors.forEach((e) => {
          const field = e.loc[e.loc.length - 1];
          newErrors[field] = e.msg;
        });
        setErrors(newErrors);
      }
    },
  });

  const validate = () => {
    const newErrors = {};

    if (!form.title || form.title.length < 5) {
      newErrors.title = 'Title must be at least 5 characters';
    }
    if (!form.description || form.description.length < 50) {
      newErrors.description = `Description must be at least 50 characters (currently ${form.description?.length || 0})`;
    }
    if (!form.category_id) {
      newErrors.category_id = 'Please select a category';
    }
    if (!form.budget_min || parseFloat(form.budget_min) <= 0) {
      newErrors.budget_min = 'Must be a positive number';
    }
    if (!form.budget_max || parseFloat(form.budget_max) <= 0) {
      newErrors.budget_max = 'Must be a positive number';
    }
    if (form.budget_min && form.budget_max && parseFloat(form.budget_min) > parseFloat(form.budget_max)) {
      newErrors.budget_max = 'Budget max must be greater than budget min';
    }
    
    if (!form.deadline) {
      newErrors.deadline = 'Deadline is required';
    } else {
      const today = new Date().toISOString().split('T')[0];
      if (form.deadline < today) {
        newErrors.deadline = 'Deadline must be today or in the future';
      }
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    mutation.mutate({
      ...form,
      category_id: parseInt(form.category_id),
      budget_min: parseFloat(form.budget_min),
      budget_max: parseFloat(form.budget_max),
    });
  };

  const update = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
    if (errors[key]) {
      setErrors((prev) => ({ ...prev, [key]: undefined }));
    }
  };

  const catOptions = (categories || []).map((c) => ({ value: c.id, label: c.name }));

  return (
    <div className="post-job-page container">
      <h1>Post a New Job</h1>
      <form onSubmit={handleSubmit} className="post-job-form">
        <Input
          label="Job Title"
          value={form.title}
          onChange={(e) => update('title', e.target.value)}
          error={errors.title}
          required
        />
        <Select
          label="Category"
          options={catOptions}
          value={form.category_id}
          onChange={(e) => update('category_id', e.target.value)}
          error={errors.category_id}
          required
        />
        <Textarea
          label="Description"
          value={form.description}
          onChange={(e) => update('description', e.target.value)}
          rows={6}
          maxLength={5000}
          error={errors.description}
          required
        />

        <div className="form-row">
          <Input
            label="Budget Min"
            type="number"
            value={form.budget_min}
            onChange={(e) => update('budget_min', e.target.value)}
            error={errors.budget_min}
            required
          />
          <Input
            label="Budget Max"
            type="number"
            value={form.budget_max}
            onChange={(e) => update('budget_max', e.target.value)}
            error={errors.budget_max}
            required
          />
        </div>

        <div className="form-row">
          <Select
            label="Pricing Model"
            options={PRICING_MODELS}
            value={form.pricing_model}
            onChange={(e) => update('pricing_model', e.target.value)}
          />
          <Select
            label="Engagement Type"
            options={ENGAGEMENT_TYPES}
            value={form.engagement_type}
            onChange={(e) => update('engagement_type', e.target.value)}
          />
        </div>

        <div className="form-row">
            <Input
              label="Deadline"
              type="date"
              value={form.deadline}
              onChange={(e) => update('deadline', e.target.value)}
              error={errors.deadline}
              min={new Date().toISOString().split('T')[0]}
              required
            />
          <Input
            label="Expected Delivery Time"
            value={form.expected_delivery_time}
            onChange={(e) => update('expected_delivery_time', e.target.value)}
            placeholder="e.g. 2 weeks"
          />
        </div>

        <div className="form-row">
          <Input
            label="Jurisdiction"
            value={form.jurisdiction}
            onChange={(e) => update('jurisdiction', e.target.value)}
            placeholder="US, UK, UAE..."
          />
          <Input
            label="Accounting Standard"
            value={form.accounting_standard}
            onChange={(e) => update('accounting_standard', e.target.value)}
            placeholder="GAAP, IFRS..."
          />
        </div>

        <label className="checkbox-label" style={{ marginTop: 8 }}>
          <input
            type="checkbox"
            checked={form.nda_required}
            onChange={(e) => update('nda_required', e.target.checked)}
          />
          NDA Required (accountants must sign NDA before viewing full details)
        </label>

        {mutation.isError && !Object.keys(errors).length && (
          <div style={{ color: 'var(--color-danger)', fontSize: 13, marginTop: 8 }}>
            Failed to create job. Please check your inputs.
          </div>
        )}

        <Button type="submit" variant="primary" size="lg" loading={mutation.isPending} style={{ marginTop: 24 }}>
          Post Job
        </Button>
      </form>
    </div>
  );
}