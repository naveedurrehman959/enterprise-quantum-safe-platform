import { useEffect, useState } from "react";
import {
    Card,
    CardContent,
    Typography,
    Chip,
    Stack,
    Box,
    Grid,
    IconButton
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";

import notificationService from "../services/notificationService";


export default function Notifications() {


const [notifications,setNotifications]=useState([]);


const loadNotifications = async()=>{

try{

const data =
await notificationService.getNotifications();


setNotifications(
data.notifications || []
);


}
catch(err){

console.error(
"Notification loading failed",
err
);

}


};



useEffect(()=>{

loadNotifications();

},[]);




return (

<>


<Box
display="flex"
justifyContent="space-between"
alignItems="center"
mb={3}
>


<Box>

<Typography
variant="h4"
>

Security Notifications

</Typography>


<Typography
color="text.secondary"
>

Security events, migration alerts,
and platform activities

</Typography>


</Box>

<IconButton
    color="primary"
    onClick={loadNotifications}
    sx={{
        border: "1px solid #d1d5db",
        borderRadius: 2
    }}
>
    <RefreshIcon />
</IconButton>




</Box>





<Chip

label={
`${notifications.length} Notifications`
}

color="primary"

sx={{mb:3}}

/>






{
notifications.length === 0 ?

(

<Card>

<CardContent>

<Typography>

No security notifications available.

</Typography>

</CardContent>

</Card>

)

:

(

<Stack spacing={2}>


{
notifications.map((n)=>(


<Card

key={n.id}

elevation={3}

>


<CardContent>


<Grid container spacing={2}>


<Grid size={{xs:12}}>


<Typography
variant="h6"
>

{n.title}

</Typography>


<Typography
color="text.secondary"
>

{n.message}

</Typography>


</Grid>





<Grid size={{xs:12}}>


<Chip

label={n.module}

sx={{mr:1}}

/>



<Chip

label={n.status}

color={
n.status === "SUCCESS"
?
"success"
:
n.status === "WARNING"
?
"warning"
:
"error"
}

/>


</Grid>





<Grid size={{xs:12}}>


<Typography
variant="body2"
>

{
new Date(
n.timestamp
).toLocaleString()
}


</Typography>


</Grid>


</Grid>



</CardContent>


</Card>


))

}



</Stack>


)

}


</>

);


}
