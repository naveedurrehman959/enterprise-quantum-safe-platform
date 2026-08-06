import {
    Card,
    CardContent,
    Typography,
    Box
} from "@mui/material";

function StatCard({
    title,
    value,
    icon,
    color = "#1976d2"
}) {

    return (

        <Card
            elevation={4}
            sx={{
                borderRadius:3,
                transition:"0.3s",
                "&:hover":{
                    transform:"translateY(-4px)"
                }
            }}
        >

            <CardContent>

                <Box
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                >

                    <Box>

                        <Typography
                            variant="subtitle2"
                            color="text.secondary"
                        >
                            {title}
                        </Typography>

                        <Typography
                            variant="h4"
                            fontWeight="bold"
                            mt={1}
                        >
                            {value}
                        </Typography>

                    </Box>

                    <Box
                        sx={{
                            width:55,
                            height:55,
                            borderRadius:"50%",
                            background:color,
                            display:"flex",
                            justifyContent:"center",
                            alignItems:"center",
                            color:"#fff",
                            fontSize:28
                        }}
                    >
                        {icon}
                    </Box>

                </Box>

            </CardContent>

        </Card>

    );

}

export default StatCard;
