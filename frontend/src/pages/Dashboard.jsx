import { useEffect, useState } from "react";

import PeopleIcon from "@mui/icons-material/People";
import ShieldIcon from "@mui/icons-material/Shield";
import VerifiedIcon from "@mui/icons-material/Verified";
import SecurityIcon from "@mui/icons-material/Security";

import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";

import StatCard from "../components/StatCard";
import SecurityScoreChart from "../components/charts/SecurityScoreChart";
import QuantumReadiness from "../components/QuantumReadiness";

import CpuChart from "../components/charts/CpuChart";
import MemoryChart from "../components/charts/MemoryChart";
import DiskChart from "../components/charts/DiskChart";

import ServiceStatusTable from "../components/charts/ServiceStatusTable";

import {
    getDashboard
} from "../services/dashboardService";

import monitoringService from "../services/monitoringService";


function Dashboard() {

    const [data, setData] = useState(null);
    const [system, setSystem] = useState(null);
    const [services, setServices] = useState({});
    const [error, setError] = useState("");


    useEffect(() => {

        async function loadDashboard(){

            try {

                const dashboard =
                    await getDashboard();

                const health =
                    await monitoringService.getSystemHealth();

                const serviceData =
                    await monitoringService.getServices();


                setData(dashboard);

                setSystem(
                    health.data
                );

                setServices(
                    serviceData.data
                );


            } catch(error){

                console.error(error);

                setError(
                    "Failed to load dashboard data."
                );

            }

        }


        loadDashboard();


        const interval =
            setInterval(
                loadDashboard,
                30000
            );


        return () =>
            clearInterval(interval);


    }, []);



    if(error){

        return (
            <Typography color="error">
                {error}
            </Typography>
        );

    }


    if(!data || !system){

        return (
            <Typography>
                Loading Dashboard...
            </Typography>
        );

    }



    return (

        <>

        <Typography
            variant="h4"
            sx={{mb:3}}
        >
            Enterprise Quantum-Safe Dashboard
        </Typography>


        <Grid container spacing={3}>


            <Grid size={{xs:12,sm:6,md:3}}>
                <StatCard
                    title="Users"
                    value={data.users}
                    icon={<PeopleIcon/>}
                    color="#1976d2"
                />
            </Grid>


            <Grid size={{xs:12,sm:6,md:3}}>
                <StatCard
                    title="Certificates"
                    value={data.certificates}
                    icon={<VerifiedIcon/>}
                    color="#2e7d32"
                />
            </Grid>


            <Grid size={{xs:12,sm:6,md:3}}>
                <StatCard
                    title="Active Sessions"
                    value={data.active_sessions}
                    icon={<ShieldIcon/>}
                    color="#ed6c02"
                />
            </Grid>


            <Grid size={{xs:12,sm:6,md:3}}>
                <StatCard
                    title="Security Alerts"
                    value={data.security_alerts}
                    icon={<SecurityIcon/>}
                    color="#d32f2f"
                />
            </Grid>



            <Grid size={{xs:12,md:8}}>

                <Paper
                    elevation={3}
                    sx={{
                        p:3,
                        borderRadius:2
                    }}
                >

                    <Typography variant="h6">
                        Enterprise Security Score
                    </Typography>


                    <SecurityScoreChart
                        score={
                            data.security_score
                        }
                    />


                </Paper>

            </Grid>



            <Grid size={{xs:12,md:4}}>

                <QuantumReadiness

                    score={
                        data.quantum_readiness_score
                    }

                />

            </Grid>




            <Grid size={{xs:12,md:4}}>

                <Paper
                    elevation={3}
                    sx={{p:2}}
                >

                    <Typography variant="h6">
                        CPU Usage
                    </Typography>

                    <CpuChart
                        value={
                            system.cpu_usage
                        }
                    />

                </Paper>

            </Grid>



            <Grid size={{xs:12,md:4}}>

                <Paper
                    elevation={3}
                    sx={{p:2}}
                >

                    <Typography variant="h6">
                        Memory Usage
                    </Typography>


                    <MemoryChart
                        value={
                            system.memory_usage
                        }
                    />

                </Paper>

            </Grid>



            <Grid size={{xs:12,md:4}}>

                <Paper
                    elevation={3}
                    sx={{p:2}}
                >

                    <Typography variant="h6">
                        Disk Usage
                    </Typography>


                    <DiskChart
                        value={
                            system.disk_usage
                        }
                    />

                </Paper>

            </Grid>



            <Grid size={{xs:12}}>

                <ServiceStatusTable
                    services={services}
                />

            </Grid>


        </Grid>


        </>

    );

}


export default Dashboard;
