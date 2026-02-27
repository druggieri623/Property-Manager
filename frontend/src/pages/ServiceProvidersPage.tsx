import { useState } from "react";

import type { ServiceProvider } from "../api";
import type { ServiceProviderPayload } from "../api";

type ServiceProvidersPageProps = {
  providers: ServiceProvider[];
  onCreate: (payload: ServiceProviderPayload) => Promise<void>;
  onUpdate: (id: number, payload: ServiceProviderPayload) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  isSubmitting: boolean;
};

const INITIAL_FORM: ServiceProviderPayload = {
  company_name: "",
  contact_name: "",
  email: "",
  phone: "",
  service_category: "",
  notes: "",
  active: true
};

export function ServiceProvidersPage({
  providers,
  onCreate,
  onUpdate,
  onDelete,
  isSubmitting
}: ServiceProvidersPageProps) {
  const [form, setForm] = useState<ServiceProviderPayload>(INITIAL_FORM);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const payload: ServiceProviderPayload = {
      ...form,
      contact_name: form.contact_name?.trim() || undefined,
      email: form.email?.trim() || undefined,
      phone: form.phone?.trim() || undefined,
      service_category: form.service_category?.trim() || undefined,
      notes: form.notes?.trim() || undefined
    };
    try {
      if (editingId === null) {
        await onCreate(payload);
      } else {
        await onUpdate(editingId, payload);
      }
      setForm(INITIAL_FORM);
      setEditingId(null);
      setErrorMessage("");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Unable to save service provider"
      );
    }
  };

  const startEdit = (provider: ServiceProvider) => {
    setEditingId(provider.id);
    setForm({
      company_name: provider.company_name,
      contact_name: provider.contact_name ?? "",
      email: "",
      phone: provider.phone ?? "",
      service_category: provider.service_category ?? "",
      notes: "",
      active: provider.active
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm(INITIAL_FORM);
    setErrorMessage("");
  };

  const handleDelete = async (provider: ServiceProvider) => {
    const confirmed = window.confirm(
      `Delete service provider ${provider.company_name}? This cannot be undone.`
    );
    if (!confirmed) {
      return;
    }
    try {
      await onDelete(provider.id);
      setErrorMessage("");
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Unable to delete service provider"
      );
    }
  };

  return (
    <div className="card">
      <h2 className="title">Service Providers</h2>
      {errorMessage && <p className="error-text">{errorMessage}</p>}
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Company
          <input
            required
            value={form.company_name}
            onChange={(event) => setForm({ ...form, company_name: event.target.value })}
          />
        </label>
        <label>
          Contact
          <input
            value={form.contact_name}
            onChange={(event) => setForm({ ...form, contact_name: event.target.value })}
          />
        </label>
        <label>
          Email
          <input
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
          />
        </label>
        <label>
          Phone
          <input
            value={form.phone}
            onChange={(event) => setForm({ ...form, phone: event.target.value })}
          />
        </label>
        <label>
          Category
          <input
            value={form.service_category}
            onChange={(event) => setForm({ ...form, service_category: event.target.value })}
          />
        </label>
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={form.active}
            onChange={(event) => setForm({ ...form, active: event.target.checked })}
          />
          Active
        </label>
        <div className="actions-row">
          <button type="submit" disabled={isSubmitting}>
            {editingId === null ? "Add Provider" : "Save Provider"}
          </button>
          {editingId !== null && (
            <button type="button" onClick={cancelEdit} disabled={isSubmitting}>
              Cancel
            </button>
          )}
        </div>
      </form>
      <table>
        <thead>
          <tr>
            <th>Company</th>
            <th>Contact</th>
            <th>Phone</th>
            <th>Category</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {providers.map((provider) => (
            <tr key={provider.id}>
              <td>{provider.company_name}</td>
              <td>{provider.contact_name ?? "-"}</td>
              <td>{provider.phone ?? "-"}</td>
              <td>{provider.service_category ?? "-"}</td>
              <td>
                <button
                  type="button"
                  onClick={() => startEdit(provider)}
                  disabled={isSubmitting}
                >
                  Edit
                </button>
                <button
                  type="button"
                  onClick={() => handleDelete(provider)}
                  disabled={isSubmitting}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
