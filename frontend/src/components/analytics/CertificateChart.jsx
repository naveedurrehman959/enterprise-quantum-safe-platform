import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

const COLORS = [
  "#1976d2",
  "#2e7d32",
  "#ef6c00",
];

function CertificateChart({ data }) {

  const chartData = [
    {
      name: "PQC",
      value: data.pqc_certificates,
    },
    {
      name: "Classical",
      value: data.classical_certificates,
    },
    {
      name: "Expired",
      value: data.expired_certificates,
    },
  ];

  return (
    <ResponsiveContainer
      width="100%"
      height={320}
    >
      <PieChart>
        <Pie
          data={chartData}
          dataKey="value"
          nameKey="name"
          outerRadius={110}
          label
        >
          {chartData.map((entry, index) => (
            <Cell
              key={index}
              fill={COLORS[index % COLORS.length]}
            />
          ))}
        </Pie>

        <Tooltip />

        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default CertificateChart;
