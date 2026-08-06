import {

    RadialBarChart,
    RadialBar,
    PolarAngleAxis,
    ResponsiveContainer

} from "recharts";

export default function SecurityScoreChart({

    score=0

}){

    return(

        <ResponsiveContainer
            width="100%"
            height={320}
        >

            <RadialBarChart

                innerRadius="70%"
                outerRadius="100%"
                data={[
                    {
                        value:score
                    }
                ]}

                startAngle={90}
                endAngle={-270}

            >

                <PolarAngleAxis
                    type="number"
                    domain={[0,100]}
                    tick={false}
                />

                <RadialBar
                    dataKey="value"
                    fill="#2563eb"
                    cornerRadius={12}
                    animationDuration={1800}
                />

                <text

                    x="50%"
                    y="50%"
                    textAnchor="middle"
                    dominantBaseline="middle"
                    fontSize="34"
                    fontWeight="bold"

                >
                    {score}%

                </text>

            </RadialBarChart>

        </ResponsiveContainer>

    );

}
