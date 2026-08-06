import {
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
  PolarAngleAxis,
} from "recharts";

function DiskChart({ value }) {
  const data = [
    {
      value,
      fill: "#ed6c02",
    },
  ];

  return (
    <ResponsiveContainer width="100%" height={260}>
      <RadialBarChart
        data={data}
        innerRadius="70%"
        outerRadius="100%"
        startAngle={90}
        endAngle={-270}
      >
        <PolarAngleAxis
          type="number"
          domain={[0, 100]}
          tick={false}
        />

        <RadialBar dataKey="value" />

        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dominantBaseline="middle"
          fontSize="28"
          fontWeight="bold"
        >
          {value}%
        </text>
      </RadialBarChart>
    </ResponsiveContainer>
  );
}

export default DiskChart;
