import { useEffect, useState } from "react";

import {
  Grid,
  Paper,
  Typography,
  Chip,
  Box,
  Card,
  CardContent,
  Alert
} from "@mui/material";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import BlockIcon from "@mui/icons-material/Block";

import policyService from "../services/policyService";


function Policy() {

  const [policy,setPolicy] = useState(null);


  useEffect(()=>{

    policyService
      .getStatus()
      .then((res)=>{

        setPolicy(res.data);

      })
      .catch(console.error);


  },[]);



  if(!policy){

    return (

      <>

        <Typography>
          Loading Policy Engine...
        </Typography>

      </>

    );

  }



  return (

    <>


      <Typography
        variant="h4"
        sx={{mb:3}}
      >

        Cryptographic Policy Engine

      </Typography>



      <Grid container spacing={3}>


        {/* Policy Status */}

        <Grid size={{xs:12}}>


          <Card
            elevation={3}
          >

            <CardContent>


              <Typography
                variant="h6"
              >

                Security Policy Status

              </Typography>


              <Box sx={{mt:2}}>


                <Alert
                  severity="success"
                  icon={<CheckCircleIcon/>}
                >

                  Policy Engine Active -
                  Cryptographic enforcement enabled

                </Alert>


              </Box>



              <Typography sx={{mt:2}}>

                <strong>
                Policy Name:
                </strong>

                {" "}

                {
                  policy.policy_name ||
                  "Enterprise PQC Policy"
                }

              </Typography>



              <Typography sx={{mt:1}}>

                <strong>
                Security Level:
                </strong>

                {" "}

                {
                  policy.security_level ||
                  "HIGH"
                }

              </Typography>


            </CardContent>

          </Card>


        </Grid>





        {/* Allowed Algorithms */}


        <Grid size={{xs:12,md:6}}>


          <Paper
            elevation={3}
            sx={{
              p:3,
              minHeight:250
            }}
          >


            <Typography
              variant="h6"
              gutterBottom
            >

              Approved Algorithms

            </Typography>



            {
              (
                policy.approved_algorithms ||
                policy.allowed_algorithms ||
                []
              )
              .map((algorithm)=>(


                <Chip

                  key={algorithm}

                  label={algorithm}

                  color="success"

                  icon={
                    <CheckCircleIcon/>
                  }

                  sx={{
                    mr:1,
                    mb:1
                  }}

                />


              ))

            }



          </Paper>


        </Grid>






        {/* Blocked Algorithms */}


        <Grid size={{xs:12,md:6}}>


          <Paper
            elevation={3}
            sx={{
              p:3,
              minHeight:250
            }}
          >


            <Typography
              variant="h6"
              gutterBottom
            >

              Blocked Algorithms

            </Typography>



            {
              (
                policy.blocked_algorithms ||
                []
              )
              .map((algorithm)=>(


                <Chip

                  key={algorithm}

                  label={algorithm}

                  color="error"

                  icon={
                    <BlockIcon/>
                  }

                  sx={{
                    mr:1,
                    mb:1
                  }}

                />


              ))

            }



          </Paper>


        </Grid>



      </Grid>



    </>

  );

}


export default Policy;
