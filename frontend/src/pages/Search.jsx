import { useState } from "react";

import {
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Box,
  CircularProgress,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";

import searchService from "../services/searchService";


export default function Search() {


  const [query,setQuery] = useState("");

  const [results,setResults] = useState(null);

  const [loading,setLoading] = useState(false);



  const handleSearch = async()=>{


    if(!query)
      return;


    try{

      setLoading(true);


      const data =
        await searchService.search(query);


      setResults(data);


    }
    catch(error){

      console.error(
        "Search failed",
        error
      );

    }
    finally{

      setLoading(false);

    }


  };




  return (

    <>


      <Typography
        variant="h4"
        sx={{mb:1}}
      >

        Enterprise Search

      </Typography>


      <Typography
        color="text.secondary"
        sx={{mb:3}}
      >

        Search users, cryptographic assets,
        certificates and audit events

      </Typography>





      <Box
        display="flex"
        gap={2}
      >

        <TextField

          fullWidth

          label="Search cryptographic assets"

          value={query}

          onChange={
            e=>setQuery(
              e.target.value
            )
          }

        />


        <Button

          variant="contained"

          startIcon={<SearchIcon/>}

          onClick={handleSearch}

        >

          Search

        </Button>


      </Box>






      {
        loading &&

        <Box
          textAlign="center"
          mt={5}
        >

          <CircularProgress/>

        </Box>

      }






      {
      results &&

      <Grid
        container
        spacing={3}
        mt={2}
      >



      <Grid item xs={12}>

        <Card>

          <CardContent>


          <Typography variant="h6">

            Search Summary

          </Typography>


          <Box mt={2}>


            <Chip

              label={
                `Users: ${
                  results.users?.length || 0
                }`
              }

              sx={{mr:1}}

            />


            <Chip

              label={
                `Algorithms: ${
                  results.algorithms?.length || 0
                }`
              }

              sx={{mr:1}}

            />


            <Chip

              label={
                `Certificates: ${
                  results.certificates?.length || 0
                }`
              }

              sx={{mr:1}}

            />


            <Chip

              label={
                `Audit Logs: ${
                  results.audit_logs?.length || 0
                }`
              }

            />


          </Box>


          </CardContent>

        </Card>

      </Grid>







      <Grid item xs={12}>


      <Card>


      <CardContent>


      <Typography variant="h6">

        Algorithms

      </Typography>


      <Divider sx={{my:2}}/>


      {
        results.algorithms?.map(
          (algo,index)=>(

          <Box
            key={index}
            mb={2}
          >

          <Typography>

            <strong>
              {algo.algorithm_name}
            </strong>

          </Typography>


          <Chip

            label={
              algo.status ||
              "UNKNOWN"
            }

            color={
              algo.status==="SAFE"
              ?
              "success"
              :
              "error"
            }

            size="small"

          />


          </Box>

        ))
      }


      </CardContent>


      </Card>


      </Grid>








      <Grid item xs={12}>


      <Card>


      <CardContent>


      <Typography variant="h6">

        Certificates

      </Typography>


      <Divider sx={{my:2}}/>

      
      <Table>


      <TableHead>

      <TableRow>

      <TableCell>
      Type
      </TableCell>

      <TableCell>
      Algorithm
      </TableCell>

      <TableCell>
      Status
      </TableCell>

      </TableRow>

      </TableHead>



      <TableBody>


      {
      results.certificates?.map(
        (cert,index)=>(

        <TableRow key={index}>


        <TableCell>
          {cert.type}
        </TableCell>


        <TableCell>
          {cert.algorithm}
        </TableCell>


        <TableCell>

        <Chip
          label="ACTIVE"
          color="success"
          size="small"
        />

        </TableCell>


        </TableRow>


      ))

      }


      </TableBody>


      </Table>


      </CardContent>


      </Card>


      </Grid>







      <Grid item xs={12}>


      <Card>


      <CardContent>


      <Typography variant="h6">

        Audit Events

      </Typography>


      <Divider sx={{my:2}}/>


      {
        results.audit_logs?.map(
          (log,index)=>(

          <Typography
            key={index}
            sx={{mb:1}}
          >

          {log.action}
          {" - "}
          {log.status}

          </Typography>


        ))

      }


      </CardContent>


      </Card>


      </Grid>




      </Grid>

      }



    </>

  );

}
