import {useEffect,useState} from "react";

import {
 Card,
 CardContent,
 Typography,
 Button,
 TextField,
 Stack,
 Chip
} from "@mui/material";


import vaultService from "../services/vaultService";


function Vault(){

const [status,setStatus]=useState(null);
const [secrets,setSecrets]=useState([]);

const [secret,setSecret]=useState({
 secret_name:"",
 secret_value:"",
 secret_type:"KEY"
});


const loadVault=async()=>{

try{

const s =
await vaultService.getStatus();

setStatus(s.data);


const l =
await vaultService.listSecrets();

setSecrets(
l.data.secrets || []
);


}
catch(err){

console.error(err);

}

};



useEffect(()=>{

loadVault();

},[]);



const store=async()=>{

await vaultService.storeSecret(secret);

setSecret({
 secret_name:"",
 secret_value:"",
 secret_type:"KEY"
});

loadVault();

};



return(

<>


<Typography
variant="h4"
sx={{mb:3}}
>
Enterprise Vault
</Typography>



{
status &&

<Card sx={{mb:3}}>

<CardContent>

<Typography variant="h6">
Vault Status
</Typography>


<Chip
label={status.status}
color="success"
/>


<Typography sx={{mt:2}}>
Encryption: {status.encryption}
</Typography>


<Typography>
Key Management: {status.key_management}
</Typography>


</CardContent>

</Card>

}



<Card>

<CardContent>


<Typography variant="h6">
Store Secret
</Typography>



<Stack spacing={2} sx={{mt:2}}>


<TextField
label="Secret Name"
value={secret.secret_name}
onChange={
e=>setSecret({
...secret,
secret_name:e.target.value
})
}
/>



<TextField
label="Secret Value"
type="password"
value={secret.secret_value}
onChange={
e=>setSecret({
...secret,
secret_value:e.target.value
})
}
/>



<Button
variant="contained"
onClick={store}
>
Store Secret
</Button>


</Stack>


</CardContent>

</Card>



<Card sx={{mt:3}}>

<CardContent>


<Typography variant="h6">
Secret Inventory
</Typography>


{
secrets.map((s)=>(

<Chip
key={s}
label={s}
sx={{m:1}}
/>

))

}


</CardContent>

</Card>



</>

);

}


export default Vault;
