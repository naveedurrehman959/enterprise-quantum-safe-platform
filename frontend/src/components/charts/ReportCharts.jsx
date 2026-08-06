import { Grid, Card, CardContent, Typography } from "@mui/material";

import {
  BarChart,
  PieChart
} from "@mui/x-charts";

function ReportCharts({
  migration,
  risk,
  audit
}) {


  return (

    <Grid container spacing={3}>


      {/* Migration Chart */}

      <Grid item xs={12} md={6}>

        <Card>

          <CardContent>

            <Typography variant="h6">
              Migration Progress
            </Typography>


            <BarChart

              xAxis={[
                {
                  scaleType:"band",
                  data:[
                    "Migrated",
                    "Pending"
                  ]
                }
              ]}


              series={[
                {
                  data:[
                    migration.migrated_assets,
                    migration.pending_assets
                  ]
                }
              ]}


              height={300}

            />


          </CardContent>

        </Card>

      </Grid>




      {/* Risk Chart */}

      <Grid item xs={12} md={6}>


        <Card>

          <CardContent>


            <Typography variant="h6">

              Risk Distribution

            </Typography>



            <PieChart

              series={[
                {
                  data:[

                    {
                      id:0,
                      value:risk.critical_risk,
                      label:"Critical"
                    },

                    {
                      id:1,
                      value:risk.high_risk,
                      label:"High"
                    },

                    {
                      id:2,
                      value:risk.medium_risk,
                      label:"Medium"
                    },

                    {
                      id:3,
                      value:risk.safe_assets,
                      label:"Safe"
                    }

                  ]
                }
              ]}


              height={300}

            />


          </CardContent>

        </Card>


      </Grid>




      {/* Audit Chart */}

      <Grid item xs={12}>


        <Card>


          <CardContent>


            <Typography variant="h6">

              Audit Activity

            </Typography>



            <BarChart

              xAxis={[
                {
                  scaleType:"band",
                  data:[
                    "Successful",
                    "Failed"
                  ]
                }
              ]}


              series={[
                {
                  data:[

                    audit.successful_events,

                    audit.failed_events

                  ]
                }
              ]}


              height={300}

            />


          </CardContent>


        </Card>


      </Grid>


    </Grid>

  );

}


export default ReportCharts;
