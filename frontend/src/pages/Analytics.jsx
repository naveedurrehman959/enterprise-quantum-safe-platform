import { useEffect, useState } from "react";

import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import Box from "@mui/material/Box";

import monitoringService from "../services/monitoringService";

import RiskPieChart from "../components/analytics/RiskPieChart";
import AlgorithmBarChart from "../components/analytics/AlgorithmBarChart";
import CertificateChart from "../components/analytics/CertificateChart";
import MigrationProgress from "../components/analytics/MigrationProgress";


function Analytics() {


const [crypto,setCrypto]=useState(null);
const [quantum,setQuantum]=useState(null);
const [pki,setPki]=useState(null);



useEffect(()=>{


Promise.all([

monitoringService.getCryptoMetrics(),

monitoringService.getQuantumReadiness(),

monitoringService.getPKIStatus()


])
.then(([cryptoRes,quantumRes,pkiRes])=>{


setCrypto(cryptoRes.data);

setQuantum(quantumRes.data);

setPki(pkiRes.data);


})
.catch(console.error);


},[]);




if(!crypto || !quantum || !pki){

return (

<Typography>
Loading Analytics...
</Typography>

);

}



return (

<>


<Typography
variant="h4"
sx={{mb:1}}
>

Enterprise Analytics Dashboard

</Typography>


<Typography
color="text.secondary"
sx={{mb:3}}
>

Cryptographic posture, migration status,
risk intelligence and certificate analytics

</Typography>



<Box sx={{mb:3}}>


<Chip

label={
`Quantum Readiness ${quantum.quantum_readiness_score}%`
}

color="primary"

sx={{mr:1}}

/>



<Chip

label={
`PQC Algorithms ${crypto.pqc_algorithms}`
}

color="success"

sx={{mr:1}}

 />



<Chip

label={
`Certificates ${pki.total_certificates}`
}

color="secondary"

/>


</Box>





<Grid container spacing={3}>


<Grid size={{xs:12,md:6}}>

<Paper sx={{p:3}} elevation={3}>


<Typography
variant="h6"
sx={{mb:2}}
>

Risk Distribution

</Typography>


<RiskPieChart

data={quantum.risk_summary}

/>


</Paper>


</Grid>





<Grid size={{xs:12,md:6}}>

<Paper sx={{p:3}} elevation={3}>


<Typography
variant="h6"
sx={{mb:2}}
>

Algorithm Distribution

</Typography>


<AlgorithmBarChart

data={crypto}

/>


</Paper>


</Grid>






<Grid size={{xs:12,md:6}}>

<Paper sx={{p:3}} elevation={3}>


<Typography
variant="h6"
sx={{mb:2}}
>

Certificate Analytics

</Typography>


<CertificateChart

data={pki}

/>


</Paper>


</Grid>






<Grid size={{xs:12,md:6}}>

<Paper sx={{p:3}} elevation={3}>


<Typography
variant="h6"
sx={{mb:2}}
>

Migration Progress

</Typography>


<MigrationProgress

safe={quantum.assets.safe}

vulnerable={quantum.assets.vulnerable}

/>


</Paper>


</Grid>



</Grid>


</>

);


}


export default Analytics;
