import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Grid,
  TextField,
  Switch,
  FormControlLabel,
  Button,
  MenuItem,
  Snackbar,
  Alert,
  Divider,
  Box,
  Chip,
} from "@mui/material";

import SaveIcon from "@mui/icons-material/Save";

import settingsService from "../services/settingsService";


function Settings() {


  const [settings,setSettings] = useState(null);

  const [saved,setSaved] = useState(false);



  useEffect(()=>{

    settingsService
      .getSettings()
      .then(res=>{

        setSettings(res.data);

      })
      .catch(console.error);


  },[]);




  if(!settings){

    return (

      <Typography>
        Loading Settings...
      </Typography>

    );

  }





  const update = (key,value)=>{

    setSettings({

      ...settings,

      [key]:value

    });

  };





  const saveSettings=()=>{

    settingsService
      .updateSettings(settings)
      .then(()=>{

        setSaved(true);

      })
      .catch(console.error);

  };





  return (

    <Box>


      <Typography
        variant="h4"
        sx={{mb:3}}
      >

        Platform Settings

      </Typography>





      <Grid container spacing={3}>




        <Grid size={{xs:12,md:6}}>


          <Paper
            elevation={3}
            sx={{p:3}}
          >


            <Typography variant="h6">

              General Configuration

            </Typography>


            <Divider sx={{my:2}}/>




            <TextField

              fullWidth

              label="Theme"

              select

              value={
                settings.theme
              }

              onChange={
                e=>
                update(
                  "theme",
                  e.target.value
                )
              }

              sx={{mb:3}}

            >

              <MenuItem value="light">

                Light

              </MenuItem>


              <MenuItem value="dark">

                Dark

              </MenuItem>


            </TextField>





            <TextField

              fullWidth

              label="Dashboard Refresh Interval"

              type="number"

              value={
                settings.dashboard_refresh
              }

              onChange={
                e=>
                update(
                  "dashboard_refresh",
                  Number(e.target.value)
                )
              }

            />



          </Paper>


        </Grid>





        <Grid size={{xs:12,md:6}}>


          <Paper
            elevation={3}
            sx={{p:3}}
          >


            <Typography variant="h6">

              Quantum Security Policy

            </Typography>


            <Divider sx={{my:2}}/>




            <TextField

              fullWidth

              label="Default PQC Algorithm"

              select

              value={
                settings.default_algorithm
              }

              onChange={
                e=>
                update(
                  "default_algorithm",
                  e.target.value
                )
              }

            >

              <MenuItem value="ML-KEM-768">

                ML-KEM-768

              </MenuItem>


              <MenuItem value="ML-KEM-1024">

                ML-KEM-1024

              </MenuItem>


            </TextField>



            <Box mt={2}>

              <Chip

                label="NIST PQC Enabled"

                color="success"

              />

            </Box>


          </Paper>


        </Grid>







        <Grid size={{xs:12,md:6}}>


          <Paper
            elevation={3}
            sx={{p:3}}
          >


            <Typography variant="h6">

              Risk Management

            </Typography>


            <Divider sx={{my:2}}/>




            <TextField

              fullWidth

              label="Risk Threshold"

              select

              value={
                settings.risk_threshold
              }

              onChange={
                e=>
                update(
                  "risk_threshold",
                  e.target.value
                )
              }

            >

              <MenuItem value="LOW">
                LOW
              </MenuItem>


              <MenuItem value="MEDIUM">
                MEDIUM
              </MenuItem>


              <MenuItem value="HIGH">
                HIGH
              </MenuItem>


            </TextField>


          </Paper>


        </Grid>







        <Grid size={{xs:12,md:6}}>


          <Paper
            elevation={3}
            sx={{p:3}}
          >


            <Typography variant="h6">

              Automation Controls

            </Typography>


            <Divider sx={{my:2}}/>


            <FormControlLabel

              control={

                <Switch

                  checked={
                    settings.notifications
                  }

                  onChange={
                    e=>
                    update(
                      "notifications",
                      e.target.checked
                    )
                  }

                />

              }

              label="Security Notifications"

            />



            <br/>




            <FormControlLabel

              control={

                <Switch

                  checked={
                    settings.auto_migration
                  }

                  onChange={
                    e=>
                    update(
                      "auto_migration",
                      e.target.checked
                    )
                  }

                />

              }

              label="Automatic PQC Migration"

            />


          </Paper>


        </Grid>


      </Grid>





      <Button

        variant="contained"

        startIcon={<SaveIcon/>}

        sx={{
          mt:3
        }}

        onClick={saveSettings}

      >

        Save Configuration

      </Button>





      <Snackbar

        open={saved}

        autoHideDuration={3000}

        onClose={
          ()=>setSaved(false)
        }

      >

        <Alert severity="success">

          Settings saved successfully

        </Alert>


      </Snackbar>



    </Box>


  );


}


export default Settings;
