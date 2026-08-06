function DashboardCard({ title, value }) {
  return (
    <div
      style={{
        background: "#ffffff",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        minWidth: "220px",
      }}
    >
      <h3>{title}</h3>

      <h2>{value}</h2>
    </div>
  );
}

export default DashboardCard;
