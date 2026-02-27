import { useState } from "react";

import type { Owner } from "../api";
import type { OwnerPayload } from "../api";

type OwnersPageProps = {
  owners: Owner[];
  onCreate: (payload: OwnerPayload) => Promise<void>;
  onUpdate: (id: number, payload: OwnerPayload) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  isSubmitting: boolean;
};

const INITIAL_FORM: OwnerPayload = {
  unit_number: "",
  full_name: "",
  email: "",
  phone: "",
  mailing_address: "",
  dues_payment_method: "check",
  active: true
};

export function OwnersPage({
  owners,
  onCreate,
  onUpdate,
  onDelete,
  isSubmitting
}: OwnersPageProps) {
  const [form, setForm] = useState<OwnerPayload>(INITIAL_FORM);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const payload: OwnerPayload = {
      ...form,
      email: form.email?.trim() || undefined,
      phone: form.phone?.trim() || undefined,
      mailing_address: form.mailing_address?.trim() || undefined
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
      setErrorMessage(error instanceof Error ? error.message : "Unable to save owner");
    }
  };

  const startEdit = (owner: Owner) => {
    setEditingId(owner.id);
    setForm({
      unit_number: owner.unit_number,
      full_name: owner.full_name,
      email: owner.email ?? "",
      phone: owner.phone ?? "",
      mailing_address: "",
      dues_payment_method: owner.dues_payment_method,
      active: owner.active
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setForm(INITIAL_FORM);
    setErrorMessage("");
  };

  const handleDelete = async (owner: Owner) => {
    const confirmed = window.confirm(
      `Delete owner for unit ${owner.unit_number}? This cannot be undone.`
    );
    if (!confirmed) {
      return;
    }
    try {
      await onDelete(owner.id);
      setErrorMessage("");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Unable to delete owner");
    }
  };

  return (
    <div className="card">
      <h2 className="title">Owners</h2>
      {errorMessage && <p className="error-text">{errorMessage}</p>}
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Unit
          <input
            required
            value={form.unit_number}
            onChange={(event) => setForm({ ...form, unit_number: event.target.value })}
          />
        </label>
        <label>
          Full Name
          <input
            required
            value={form.full_name}
            onChange={(event) => setForm({ ...form, full_name: event.target.value })}
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
          Dues Method
          <select
            value={form.dues_payment_method}
            onChange={(event) =>
              setForm({ ...form, dues_payment_method: event.target.value })
            }
          >
            <option value="check">check</option>
            <option value="ach">ach</option>
            <option value="online">online</option>
          </select>
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
            {editingId === null ? "Add Owner" : "Save Owner"}
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
            <th>Unit</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Dues Method</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {owners.map((owner) => (
            <tr key={owner.id}>
              <td>{owner.unit_number}</td>
              <td>{owner.full_name}</td>
              <td>{owner.email ?? "-"}</td>
              <td>{owner.phone ?? "-"}</td>
              <td>{owner.dues_payment_method}</td>
              <td>
                <button type="button" onClick={() => startEdit(owner)} disabled={isSubmitting}>
                  Edit
                </button>
                <button
                  type="button"
                  onClick={() => handleDelete(owner)}
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
