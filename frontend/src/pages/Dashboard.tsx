type DashboardProps = {
  bankName?: string;
  duesCollectionMethod?: string;
};

export function Dashboard({ bankName, duesCollectionMethod }: DashboardProps) {
  return (
    <div className="card">
      <h2 className="title">Dashboard</h2>
      <p className="muted">HOA units: 11</p>
      <p>Bank: {bankName ?? "Loading..."}</p>
      <p>Dues collection: {duesCollectionMethod ?? "Loading..."}</p>
    </div>
  );
}
