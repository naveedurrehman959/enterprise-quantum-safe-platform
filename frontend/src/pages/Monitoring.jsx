import { useEffect, useState } from "react";

import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import Alert from "@mui/material/Alert";

import monitoringService from "../services/monitoringService";

import CpuChart from "../components/charts/CpuChart";
import MemoryChart from "../components/charts/MemoryChart";
import DiskChart from "../components/charts/DiskChart";
import SecurityScoreChart from "../components/charts/SecurityScoreChart";
import ServiceStatusTable from "../components/charts/ServiceStatusTable";


function Monitoring() {

const [data,setData] = useState(null);


useEffect(()=>{

const load = async()=>{

try{

const [
dashboard,
system,
crypto,
platform,
quantum,
pki,
vault
]= await Promise.all([

monitoringService.getDashboard(),
monitoringService.getSystemHealth(),
monitoringService.getCryptoMetrics(),
monitoringService.getPlatformStatus(),
monitoringService.getQuantumReadiness(),
monitoringService.getPKIStatus(),
monitoringService.getVaultStatus()

]);


setData({

dashboard:dashboard.data,
system:system.data,
crypto:crypto.data,
platform:platform.data,
quantum:quantum.data,
pki:pki.data,
vault:vault.data

});


}
catch(error){

console.error(error);

}

};


load();


const interval=setInterval(
load,
5000
);


return ()=>clearInterval(interval);


},[]);



if(!data){

return (
<Typography>
Loading Monitoring Dashboard...
</Typography>
);

}



return (

<>

<Typography
variant="h4"
sx={{mb:3}}
>
Enterprise Monitoring Dashboard
</Typography>



<Grid container spacing={3}>


<Grid size={{xs:12,md:3}}>
<Paper sx={{p:2}}>

<Typography align="center">
CPU Usage
</Typography>

<CpuChart
value={data.system.cpu_usage}
/>

</Paper>
</Grid>



<Grid size={{xs:12,md:3}}>
<Paper sx={{p:2}}>

<Typography align="center">
Memory Usage
</Typography>

<MemoryChart
value={data.system.memory_usage}
/>

</Paper>
</Grid>



<Grid size={{xs:12,md:3}}>
<Paper sx={{p:2}}>

<Typography align="center">
Disk Usage
</Typography>

<DiskChart
value={data.system.disk_usage}
/>

</Paper>
</Grid>




<Grid size={{xs:12,md:3}}>
<Paper sx={{p:2}}>

<Typography align="center">
Quantum Score
</Typography>

<SecurityScoreChart
score={
data.dashboard.security_score
}
/>

</Paper>
</Grid>





<Grid size={{xs:12,md:6}}>

<Paper sx={{p:3}}>

<Typography variant="h6">
Platform Services
</Typography>


<ServiceStatusTable
services={
data.platform.services
}
/>


</Paper>

</Grid>




<Grid size={{xs:12,md:6}}>

<Paper sx={{p:3}}>

<Typography variant="h6">
Quantum Readiness
</Typography>


<Typography>
Score:
{data.quantum.quantum_readiness_score}%
</Typography>


<Typography>
Safe Assets:
{data.quantum.assets.safe}
</Typography>


<Typography>
Vulnerable Assets:
{data.quantum.assets.vulnerable}
</Typography>


{
data.quantum.migration_required &&

<Alert severity="warning" sx={{mt:2}}>

{data.quantum.recommendation}

</Alert>

}


</Paper>

</Grid>




<Grid size={{xs:12,md:4}}>

<Paper sx={{p:3}}>

<Typography variant="h6">
Crypto Metrics
</Typography>


<Typography>
Total Algorithms:
{data.crypto.total_algorithms}
</Typography>


<Typography>
PQC:
{data.crypto.pqc_algorithms}
</Typography>


<Typography>
Classical:
{data.crypto.classical_algorithms}
</Typography>


</Paper>

</Grid>





<Grid size={{xs:12,md:4}}>

<Paper sx={{p:3}}>

<Typography variant="h6">
PKI Status
</Typography>


<Typography>
Certificates:
{data.pki.total_certificates}
</Typography>


<Typography>
PQC Certificates:
{data.pki.pqc_certificates}
</Typography>


<Chip
label={
data.pki.certificate_health
}
color="success"
/>


</Paper>

</Grid>




<Grid size={{xs:12,md:4}}>

<Paper sx={{p:3}}>

<Typography variant="h6">
Vault Status
</Typography>


<Typography>
Status:
{data.vault.status}
</Typography>


<Typography>
Secrets:
{data.vault.stored_secrets}
</Typography>


<Typography>
Encryption:
{data.vault.encryption}
</Typography>


</Paper>

</Grid>



</Grid>

</>

);

}


export default Monitoring;
