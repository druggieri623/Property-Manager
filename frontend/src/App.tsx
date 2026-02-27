import { useEffect, useState } from "react";

import {
  createOwner,
  createServiceProvider,
  deleteOwner,
  deleteServiceProvider,
  fetchBankSettings,
  fetchOwners,
  fetchServiceProviders,
  type Owner,
  type OwnerPayload,
  type ServiceProvider,
  type ServiceProviderPayload,
  updateOwner,
  updateServiceProvider
} from "./api";
import { Dashboard } from "./pages/Dashboard";
import { OwnersPage } from "./pages/OwnersPage";
import { ServiceProvidersPage } from "./pages/ServiceProvidersPage";

function App() {
  const [owners, setOwners] = useState<Owner[]>([]);
  const [providers, setProviders] = useState<ServiceProvider[]>([]);
  const [bankName, setBankName] = useState<string>();
  const [duesMethod, setDuesMethod] = useState<string>();
  const [isOwnerSubmitting, setIsOwnerSubmitting] = useState(false);
  const [isProviderSubmitting, setIsProviderSubmitting] = useState(false);

  const loadOwners = async () => {
    const data = await fetchOwners();
    setOwners(data);
  };

  const loadProviders = async () => {
    const data = await fetchServiceProviders();
    setProviders(data);
  };

  useEffect(() => {
    loadOwners().catch(() => setOwners([]));
    loadProviders().catch(() => setProviders([]));
    fetchBankSettings()
      .then((settings) => {
        setBankName(settings.bank_name);
        setDuesMethod(settings.dues_collection_method);
      })
      .catch(() => {
        setBankName(undefined);
        setDuesMethod(undefined);
      });
  }, []);

  const handleCreateOwner = async (payload: OwnerPayload) => {
    setIsOwnerSubmitting(true);
    try {
      await createOwner(payload);
      await loadOwners();
    } finally {
      setIsOwnerSubmitting(false);
    }
  };

  const handleUpdateOwner = async (id: number, payload: OwnerPayload) => {
    setIsOwnerSubmitting(true);
    try {
      await updateOwner(id, payload);
      await loadOwners();
    } finally {
      setIsOwnerSubmitting(false);
    }
  };

  const handleDeleteOwner = async (id: number) => {
    setIsOwnerSubmitting(true);
    try {
      await deleteOwner(id);
      await loadOwners();
    } finally {
      setIsOwnerSubmitting(false);
    }
  };

  const handleCreateProvider = async (payload: ServiceProviderPayload) => {
    setIsProviderSubmitting(true);
    try {
      await createServiceProvider(payload);
      await loadProviders();
    } finally {
      setIsProviderSubmitting(false);
    }
  };

  const handleUpdateProvider = async (id: number, payload: ServiceProviderPayload) => {
    setIsProviderSubmitting(true);
    try {
      await updateServiceProvider(id, payload);
      await loadProviders();
    } finally {
      setIsProviderSubmitting(false);
    }
  };

  const handleDeleteProvider = async (id: number) => {
    setIsProviderSubmitting(true);
    try {
      await deleteServiceProvider(id);
      await loadProviders();
    } finally {
      setIsProviderSubmitting(false);
    }
  };

  return (
    <main className="container">
      <h1>HOA Property Manager</h1>
      <Dashboard bankName={bankName} duesCollectionMethod={duesMethod} />
      <OwnersPage
        owners={owners}
        onCreate={handleCreateOwner}
        onUpdate={handleUpdateOwner}
        onDelete={handleDeleteOwner}
        isSubmitting={isOwnerSubmitting}
      />
      <ServiceProvidersPage
        providers={providers}
        onCreate={handleCreateProvider}
        onUpdate={handleUpdateProvider}
        onDelete={handleDeleteProvider}
        isSubmitting={isProviderSubmitting}
      />
    </main>
  );
}

export default App;
