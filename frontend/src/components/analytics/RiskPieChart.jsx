import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#d32f2f",
  "#f57c00",
  "#fbc02d",
  "#388e3c",
];

function RiskPieChart({ data }) {
  const chartData = [
    {
      name: "Critical",
      value: data.CRITICAL || 0,
    },
    {
      name: "High",
      value: data.HIGH || 0,
    },
    {
      name: "Medium",
      value: data.MEDIUM || 0,
    },
    {
      name: "Safe",
      value: data.SAFE || 0,
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
              fill={
                COLORS[index % COLORS.length]
              }
            />
          ))}
        </Pie>

        <Tooltip />

        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export default RiskPieChart;
