import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

function AlgorithmBarChart({ data }) {

  const chartData = [
    {
      name: "Classical",
      value: data.classical_algorithms,
    },
    {
      name: "PQC",
      value: data.pqc_algorithms,
    },
    {
      name: "Total",
      value: data.total_algorithms,
    },
  ];

  return (
    <ResponsiveContainer
      width="100%"
      height={320}
    >
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="name" />

        <YAxis allowDecimals={false} />

        <Tooltip />

        <Bar
          dataKey="value"
          fill="#1976d2"
          radius={[6, 6, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default AlgorithmBarChart;
