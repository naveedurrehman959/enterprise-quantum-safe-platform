import { useEffect, useState } from "react";

import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Divider,
  CircularProgress,
} from "@mui/material";

import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import TableViewIcon from "@mui/icons-material/TableView";

import DashboardLayout from "../layouts/DashboardLayout";
import reportService from "../services/reportService";


function Reports() {

  const [data, setData] = useState(null);


  useEffect(() => {

    const loadReports = async () => {

      try {

        const [
          summary,
          risk,
          compliance,
          migration,
          audit,
          certificates
        ] = await Promise.all([

          reportService.getSummary(),
          reportService.getRiskReport(),
          reportService.getComplianceReport(),
          reportService.getMigrationReport(),
          reportService.getAuditReport(),
          reportService.getCertificateReport()

        ]);


        setData({

          summary: summary.data,
          risk: risk.data,
          compliance: compliance.data,
          migration: migration.data,
          audit: audit.data,
          certificates: certificates.data

        });


      } catch(error){

        console.error(
          "Report loading failed",
          error
        );

      }

    };


    loadReports();


  }, []);



  const downloadPDF = async()=>{

    const response =
      await reportService.exportPDF();


    const url =
      window.URL.createObjectURL(
        new Blob([response.data])
      );


    const link =
      document.createElement("a");


    link.href=url;

    link.download =
      "quantum-security-report.pdf";


    link.click();

  };



  const downloadCSV = async()=>{

    const response =
      await reportService.exportCSV();


    const url =
      window.URL.createObjectURL(
        new Blob([response.data])
      );


    const link =
      document.createElement("a");


    link.href=url;

    link.download =
      "quantum-security-report.csv";


    link.click();

  };



  if(!data){

    return (

      <DashboardLayout>

        <Box
          display="flex"
          justifyContent="center"
          mt={10}
        >

          <CircularProgress />

        </Box>


      </DashboardLayout>

    );

  }



  return (

    <DashboardLayout>


      <Box mb={3}>


        <Typography variant="h4">

          Enterprise Quantum-Safe Reports

        </Typography>


        <Typography color="text.secondary">

          Security posture, migration,
          compliance and audit analytics

        </Typography>


        <Box mt={2}>


          <Button

            variant="contained"

            startIcon={<PictureAsPdfIcon/>}

            onClick={downloadPDF}

            sx={{mr:2}}

          >

            Export PDF

          </Button>



          <Button

            variant="outlined"

            startIcon={<TableViewIcon/>}

            onClick={downloadCSV}

          >

            Export CSV

          </Button>


        </Box>


      </Box>



      <Divider sx={{mb:3}} />



      <Grid container spacing={3}>


        <Grid item xs={12} md={3}>

          <MetricCard

            title="Total Assets"

            value={
              data.summary.total_assets
              ||
              0
            }

          />

        </Grid>



        <Grid item xs={12} md={3}>

          <MetricCard

            title="Critical Risk"

            value={
              data.risk.critical_risk
              ||
              0
            }

          />

        </Grid>



        <Grid item xs={12} md={3}>

          <MetricCard

            title="PQC Certificates"

            value={
              data.certificates.pqc_certificates
              ||
              0
            }

          />

        </Grid>



        <Grid item xs={12} md={3}>

          <MetricCard

            title="Audit Events"

            value={
              data.audit.total_events
              ||
              0
            }

          />

        </Grid>




        <Grid item xs={12}>


          <ReportCard

            title="Compliance Report"

            content={
              JSON.stringify(
                data.compliance,
                null,
                2
              )
            }

          />


        </Grid>



        <Grid item xs={12}>


          <ReportCard

            title="Migration Report"

            content={
              JSON.stringify(
                data.migration,
                null,
                2
              )
            }

          />


        </Grid>



        <Grid item xs={12}>


          <ReportCard

            title="Risk Assessment"

            content={
              JSON.stringify(
                data.risk,
                null,
                2
              )
            }

          />


        </Grid>



      </Grid>


    </DashboardLayout>

  );

}



function MetricCard({title,value}){


return (

<Card>


<CardContent>


<Typography
variant="subtitle2"
color="text.secondary"
>

{title}

</Typography>


<Typography
variant="h3"
>

{value}

</Typography>


</CardContent>


</Card>

);


}



function ReportCard({title,content}){


return (

<Card>


<CardContent>


<Typography variant="h6">

{title}

</Typography>


<pre>

{content}

</pre>


</CardContent>


</Card>

);


}



export default Reports;
