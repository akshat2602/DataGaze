import {
  Box,
  GridItem,
  Grid,
  Text,
  HStack,
  Accordion,
  AccordionPanel,
  AccordionIcon,
  AccordionButton,
  AccordionItem,
  Button,
  useColorModeValue,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { FaTable } from "react-icons/fa";
import { AiFillEyeInvisible } from "react-icons/ai";
import Header from "../../components/Navbars/Header";
function Tables() {
  const [databases, setDatabases] = useState([
    { hidden: true },
    { hidden: false },
    { hidden: true },
    { hidden: false },
    { hidden: true },
    { hidden: false },
    { hidden: true },
    { hidden: false },
  ]);
  const fetchDatabases = () => {
    //fetch databases by making API call
  };
  const onClick = (id) => {
    //handle routing to specific database tables
  };
  const onClickHide = (id) => {
    //Handle hiding and unhiding
  };
  const bg = useColorModeValue("light.100", "dark.100");

  return (
    <Box h="100vh" pt="2%" px="2%">
      <Header />

      <Text fontSize={"3xl"} fontWeight={"bold"} textAlign={"left"}>
        Test's Tables
      </Text>
      <Grid templateColumns="repeat(3, 1fr)">
        {databases.map((element, index) => {
          return (
            !element.hidden && (
              <GridItem colSpan={1} p="5%">
                <Box
                  cursor={"pointer"}
                  p="2% "
                  borderRadius={"xl"}
                  backgroundColor={"dark.100"}
                  textAlign={"left"}
                  // onClick={() => onClick(element)}
                >
                  <Grid templateColumns="repeat(14, 1fr)" fontSize={"2xl"}>
                    <GridItem colSpan={13}>
                      <HStack>
                        <FaTable />
                        <Text textAlign={"left"} fontSize={"2xl"}>
                          Table {index + 1}
                        </Text>
                        <Button>View Table</Button>
                        <Button variant={"link"}>Hide</Button>
                      </HStack>
                    </GridItem>
                  </Grid>
                </Box>
              </GridItem>
            )
          );
        })}
      </Grid>
      <Accordion allowMultiple>
        <AccordionItem>
          <h2>
            <AccordionButton>
              <HStack>
                <Box pb="3%">
                  <AiFillEyeInvisible />
                </Box>
                <Text textAlign={"left"}>Hidden Tables</Text>
              </HStack>
              <AccordionIcon />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4}>
            <Grid templateColumns="repeat(3, 1fr)">
              {databases.map((element, index) => {
                return (
                  element.hidden && (
                    <GridItem colSpan={1} p="5%">
                      <Box
                        cursor={"pointer"}
                        p="2% "
                        borderRadius={"xl"}
                        bg={bg}
                        textAlign={"left"}
                        // onClick={() => onClick(element)}
                      >
                        <Grid
                          templateColumns="repeat(14, 1fr)"
                          fontSize={"2xl"}
                        >
                          <GridItem colSpan={13}>
                            <HStack>
                              <FaTable />
                              <Text textAlign={"left"} fontSize={"2xl"}>
                                Table {index + 1}
                              </Text>
                              <Button>View Table</Button>
                              <Button variant={"link"}>Unhide</Button>
                            </HStack>
                          </GridItem>
                        </Grid>
                      </Box>
                    </GridItem>
                  )
                );
              })}
            </Grid>
          </AccordionPanel>
        </AccordionItem>
      </Accordion>
    </Box>
  );
}

export default Tables;
