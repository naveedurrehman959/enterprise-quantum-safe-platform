import { useEffect, useState } from "react";

import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Alert,
  Chip,
  Avatar,
  Divider,
} from "@mui/material";

import PersonIcon from "@mui/icons-material/Person";
import SecurityIcon from "@mui/icons-material/Security";

import profileService from "../services/profileService";


function Profile() {

  const [profile, setProfile] = useState({});
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const [password, setPassword] = useState({
    old_password: "",
    new_password: "",
  });


  useEffect(() => {
    loadProfile();
  }, []);


  const loadProfile = async () => {

    try {

      const data =
        await profileService.getProfile();

      setProfile(data);
      setEmail(data.email);

    }
    catch(error){

      console.error(error);
      setMessage("Failed to load profile");

    }

  };



  const updateEmail = async () => {

    try {

      await profileService.updateProfile({
        email,
      });

      setMessage(
        "Email updated successfully"
      );

      loadProfile();

    }
    catch(error){

      console.error(error);
      setMessage("Email update failed");

    }

  };



  const updatePassword = async () => {

    try {

      await profileService.changePassword(
        password
      );

      setMessage(
        "Password changed successfully"
      );

      setPassword({
        old_password:"",
        new_password:"",
      });

    }
    catch(error){

      console.error(error);
      setMessage(
        "Password change failed"
      );

    }

  };



  return (

    <Box>

      <Typography
        variant="h4"
        sx={{mb:3}}
      >
        User Profile
      </Typography>


      {
        message &&
        <Alert
          severity="info"
          sx={{mb:3}}
        >
          {message}
        </Alert>
      }



      <Grid container spacing={3}>


        <Grid size={{xs:12}}>


          <Card elevation={3}>

            <CardContent>


              <Box
                display="flex"
                alignItems="center"
                gap={3}
              >

                <Avatar
                  sx={{
                    width:70,
                    height:70
                  }}
                >

                  <PersonIcon fontSize="large"/>

                </Avatar>


                <Box>

                  <Typography variant="h5">

                    {profile.username}

                  </Typography>


                  <Typography
                    color="text.secondary"
                  >

                    {profile.email}

                  </Typography>


                  <Chip

                    label={
                      profile.role ||
                      "User"
                    }

                    color="primary"

                    sx={{
                      mt:1
                    }}

                  />

                </Box>


              </Box>


              <Divider sx={{my:3}}/>


              <Typography>

                <b>Account Created:</b>{" "}

                {
                  profile.created_at ||
                  "N/A"
                }

              </Typography>


            </CardContent>

          </Card>


        </Grid>





        <Grid size={{xs:12,md:6}}>


          <Card elevation={3}>

            <CardContent>


              <Typography
                variant="h6"
                gutterBottom
              >

                Update Email

              </Typography>



              <TextField

                fullWidth

                label="Email"

                value={email}

                onChange={
                  e=>setEmail(e.target.value)
                }

              />



              <Button

                variant="contained"

                sx={{mt:2}}

                onClick={updateEmail}

              >

                Save Email

              </Button>


            </CardContent>


          </Card>


        </Grid>





        <Grid size={{xs:12,md:6}}>


          <Card elevation={3}>


            <CardContent>


              <Typography
                variant="h6"
                gutterBottom
              >

                <SecurityIcon
                  sx={{
                    verticalAlign:"middle",
                    mr:1
                  }}
                />

                Security

              </Typography>



              <TextField

                fullWidth

                type="password"

                label="Current Password"

                value={
                  password.old_password
                }

                onChange={
                  e=>
                  setPassword({
                    ...password,
                    old_password:e.target.value
                  })
                }

              />



              <TextField

                fullWidth

                type="password"

                label="New Password"

                sx={{mt:2}}

                value={
                  password.new_password
                }

                onChange={
                  e=>
                  setPassword({
                    ...password,
                    new_password:e.target.value
                  })
                }

              />



              <Button

                variant="contained"

                sx={{mt:2}}

                onClick={updatePassword}

              >

                Change Password

              </Button>


            </CardContent>


          </Card>


        </Grid>


      </Grid>


    </Box>

  );

}


export default Profile;
