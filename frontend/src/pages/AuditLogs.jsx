import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  Box,
  IconButton,
  TextField,
  MenuItem,
  CircularProgress,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";

import api from "../services/api";


function AuditLogs() {


  const [logs,setLogs] = useState([]);

  const [loading,setLoading] = useState(true);

  const [filter,setFilter] = useState("ALL");

  const [search,setSearch] = useState("");




  const loadLogs = async()=>{

    try{

      setLoading(true);

      const res =
        await api.get("/audit/logs");


      setLogs(
        res.data.logs || []
      );


    }
    catch(error){

      console.error(
        "Audit loading failed",
        error
      );

    }
    finally{

      setLoading(false);

    }

  };




  useEffect(()=>{

    loadLogs();

  },[]);





  const filteredLogs =
    logs.filter((log)=>{


      const matchesStatus =
        filter==="ALL"
        ||
        log.status===filter;



      const matchesSearch =
        JSON.stringify(log)
        .toLowerCase()
        .includes(
          search.toLowerCase()
        );



      return (
        matchesStatus &&
        matchesSearch
      );


    });





  const statusColor=(status)=>{

    if(status==="SUCCESS")
      return "success";


    if(status==="WARNING")
      return "warning";


    return "error";

  };





  return (

    <Box>


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

            Audit Logs

          </Typography>


          <Typography
            color="text.secondary"
          >

            Security events and compliance audit trail

          </Typography>


        </Box>



        <IconButton

          onClick={loadLogs}

          sx={{

            border:"1px solid #ddd",

            borderRadius:2

          }}

        >

          <RefreshIcon/>

        </IconButton>


      </Box>





      <Box

        display="flex"

        gap={2}

        mb={3}

      >


        <TextField

          label="Search Logs"

          size="small"

          value={search}

          onChange={
            e=>setSearch(
              e.target.value
            )
          }

        />



        <TextField

          select

          size="small"

          label="Status"

          value={filter}

          onChange={
            e=>setFilter(
              e.target.value
            )
          }

          sx={{
            width:150
          }}

        >

          <MenuItem value="ALL">
            ALL
          </MenuItem>


          <MenuItem value="SUCCESS">
            SUCCESS
          </MenuItem>


          <MenuItem value="WARNING">
            WARNING
          </MenuItem>


          <MenuItem value="FAILED">
            FAILED
          </MenuItem>


        </TextField>



      </Box>






      <Chip

        label={
          `${filteredLogs.length} Events`
        }

        color="primary"

        sx={{mb:2}}

      />







      <Paper

        elevation={3}

        sx={{

          borderRadius:2,

          overflow:"auto"

        }}

      >


      {

      loading ?

      (

        <Box

          display="flex"

          justifyContent="center"

          p={5}

        >

          <CircularProgress/>

        </Box>

      )

      :

      (

      <Table>


        <TableHead>


          <TableRow>

            <TableCell>
              ID
            </TableCell>

            <TableCell>
              Action
            </TableCell>

            <TableCell>
              Module
            </TableCell>

            <TableCell>
              Status
            </TableCell>

            <TableCell>
              User
            </TableCell>

            <TableCell>
              Description
            </TableCell>

            <TableCell>
              Time
            </TableCell>


          </TableRow>


        </TableHead>




        <TableBody>


        {

        filteredLogs.length===0 ?

        (

          <TableRow>

            <TableCell colSpan={7} align="center">

              No audit events found

            </TableCell>

          </TableRow>

        )

        :

        (

        filteredLogs.map((log)=>(


          <TableRow key={log.id}>


            <TableCell>
              {log.id}
            </TableCell>



            <TableCell>
              {log.action}
            </TableCell>



            <TableCell>

              <Chip

                label={log.module}

                color="primary"

                size="small"

              />

            </TableCell>




            <TableCell>


              <Chip

                label={log.status}

                color={
                  statusColor(
                    log.status
                  )
                }

                size="small"

              />


            </TableCell>




            <TableCell>

              {
                log.user_id ||
                "SYSTEM"
              }

            </TableCell>




            <TableCell>

              {log.description}

            </TableCell>




            <TableCell>

              {
                new Date(
                  log.timestamp
                ).toLocaleString()
              }

            </TableCell>


          </TableRow>


        ))

        )

        }


        </TableBody>


      </Table>

      )

      }


      </Paper>


    </Box>

  );

}


export default AuditLogs;
