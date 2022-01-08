import {
  Box,
  GridItem,
  Grid,
  Text,
  HStack,
  Divider,
  useColorModeValue
} from "@chakra-ui/react";
import React, { useState } from "react";
import { ImDatabase } from "react-icons/im";
import { SiPostgresql } from "react-icons/si";
import Header from "../../components/Navbars/Header";
function Databases() {
  const [databases, setDatabases] = useState(["Hello", "it", "me"]);
  const fetchDatabases = () => {
    //fetch databases by making API call
  };
  const onClick = (id) => {
    //handle routing to specific database tables
  };
  const bg = useColorModeValue("light.100", "dark.100");

  return (
    <Box h="100vh" pt="2%" px="2%">
      <Header />
      
      <Text fontSize={"3xl"} fontWeight={"bold"} textAlign={"left"}>
        Your Databases
      </Text>
      <Grid templateColumns="repeat(3, 1fr)">
        {databases.map((element, index) => (
          <GridItem colSpan={1} p="5%">
            <Box
              cursor={"pointer"}
              p="2% "
              borderRadius={"xl"}
              bg={bg}
              textAlign={"left"}
              // onClick={() => onClick(element)}
            >
              <Grid templateColumns="repeat(14, 1fr)" fontSize={"2xl"}>
                <GridItem colSpan={13}>
                  <HStack>
                    <ImDatabase />
                    <Text textAlign={"left"} fontSize={"2xl"}>
                      Database {index + 1}
                    </Text>
                  </HStack>
                </GridItem>
                <GridItem colSpan={1} pt="15%">
                  <SiPostgresql />
                </GridItem>
              </Grid>
              <Divider my="2%" />
              <Text textAlign={"left"}>Created by: Rugved</Text>
            </Box>
          </GridItem>
        ))}
      </Grid>
    </Box>
  );
}

export default Databases;
