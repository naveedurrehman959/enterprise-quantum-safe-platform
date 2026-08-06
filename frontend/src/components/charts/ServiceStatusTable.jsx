import {
    Card,
    CardContent,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Chip
} from "@mui/material";

function ServiceStatusTable({ services = {} }) {

    return (

        <Card elevation={3}>

            <CardContent>

                <Typography
                    variant="h6"
                    gutterBottom
                >
                    Platform Services
                </Typography>

                <Table size="small">

                    <TableHead>

                        <TableRow>

                            <TableCell>Service</TableCell>
                            <TableCell>Status</TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {Object.entries(services).map(
                            ([name, status]) => (

                                <TableRow key={name}>

                                    <TableCell>
                                        {name}
                                    </TableCell>

                                    <TableCell>

                                        <Chip
                                            label={status}
                                            color={
                                                status.toLowerCase() === "running"
                                                    ? "success"
                                                    : "error"
                                            }
                                            size="small"
                                        />

                                    </TableCell>

                                </TableRow>

                            )
                        )}

                    </TableBody>

                </Table>

            </CardContent>

        </Card>

    );

}

export default ServiceStatusTable;
