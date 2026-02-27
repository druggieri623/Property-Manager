const API_BASE = "http://127.0.0.1:8000";

async function parseApiError(res: Response, fallbackMessage: string) {
  try {
    const data = await res.json();
    if (typeof data?.detail === "string") {
      return data.detail;
    }
  } catch {
    return fallbackMessage;
  }
  return fallbackMessage;
}

export interface Owner {
  id: number;
  unit_number: string;
  owner_one_full_name: string;
  owner_one_email?: string;
  owner_one_phone?: string;
  owner_one_mailing_address?: string;
  owner_two_full_name?: string;
  owner_two_email?: string;
  owner_two_phone?: string;
  owner_two_mailing_address?: string;
  dues_payment_method: string;
  active: boolean;
}

export interface OwnerPayload {
  unit_number: string;
  owner_one_full_name: string;
  owner_one_email?: string;
  owner_one_phone?: string;
  owner_one_mailing_address?: string;
  owner_two_full_name?: string;
  owner_two_email?: string;
  owner_two_phone?: string;
  owner_two_mailing_address?: string;
  dues_payment_method: string;
  active: boolean;
}

export interface ServiceProvider {
  id: number;
  company_name: string;
  contact_name?: string;
  phone?: string;
  service_category?: string;
  active: boolean;
}

export interface ServiceProviderPayload {
  company_name: string;
  contact_name?: string;
  email?: string;
  phone?: string;
  service_category?: string;
  notes?: string;
  active: boolean;
}

export async function fetchBankSettings() {
  const res = await fetch(`${API_BASE}/settings/bank`);
  return res.json();
}

export async function fetchOwners(): Promise<Owner[]> {
  const res = await fetch(`${API_BASE}/owners`);
  return res.json();
}

export async function createOwner(payload: OwnerPayload): Promise<Owner> {
  const res = await fetch(`${API_BASE}/owners`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(await parseApiError(res, "Failed to create owner"));
  }
  return res.json();
}

export async function updateOwner(id: number, payload: OwnerPayload): Promise<Owner> {
  const res = await fetch(`${API_BASE}/owners/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(await parseApiError(res, "Failed to update owner"));
  }
  return res.json();
}

export async function deleteOwner(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/owners/${id}`, {
    method: "DELETE"
  });
  if (!res.ok) {
    throw new Error(await parseApiError(res, "Failed to delete owner"));
  }
}

export async function fetchServiceProviders(): Promise<ServiceProvider[]> {
  const res = await fetch(`${API_BASE}/service-providers`);
  return res.json();
}

export async function createServiceProvider(
  payload: ServiceProviderPayload
): Promise<ServiceProvider> {
  const res = await fetch(`${API_BASE}/service-providers`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(await parseApiError(res, "Failed to create service provider"));
  }
  return res.json();
}

export async function updateServiceProvider(
  id: number,
  payload: ServiceProviderPayload
): Promise<ServiceProvider> {
  const res = await fetch(`${API_BASE}/service-providers/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    throw new Error(await parseApiError(res, "Failed to update service provider"));
  }
  return res.json();
}

export async function deleteServiceProvider(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/service-providers/${id}`, {
    method: "DELETE"
  });
  if (!res.ok) {
    throw new Error(await parseApiError(res, "Failed to delete service provider"));
  }
}
