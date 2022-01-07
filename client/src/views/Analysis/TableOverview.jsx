import {
  Box,
  Button,
  Flex,
  HStack,
  Text,
  Spacer,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  useDisclosure,
  DrawerCloseButton,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from "@chakra-ui/react";
import React from "react";
import Header from "../../components/Navbars/Header";
import { BsGraphUp, BsFileBarGraph, BsPieChart } from "react-icons/bs";
import { FaTable } from "react-icons/fa";
import { FiEdit2 } from "react-icons/fi";
import { IoReloadOutline } from "react-icons/io5";
import TableComponent from "./TableComponent";
function TableOverview() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = React.useRef();
  const onSave = () => {
    //Do the necessary data/filtering changes
    onClose();
  };
  return (
    <Box h="100vh" pt="2%" px="2%">
      <Header />

      <Flex mb='1%'>
        <Text fontSize={"2xl"} fontWeight={"bold"} textAlign={"left"}>
          Database | Table
        </Text>

        <Spacer />
        <HStack>
          <Button leftIcon={<FiEdit2 />} ref={btnRef} onClick={onOpen}>
            Edit
          </Button>
          <Button leftIcon={<IoReloadOutline />}>Reload</Button>
        </HStack>
      </Flex>
      {/* <Box p="2">
        <HStack>
          <Button leftIcon={<FaTable />}>Table</Button>
          <Button leftIcon={<BsGraphUp />}>Line Graph</Button>
          <Button leftIcon={<BsFileBarGraph />}>Bar Graph</Button>
          <Button leftIcon={<BsPieChart />}>Pie Chart</Button>
        </HStack>
      </Box> */}
      <Tabs isFitted variant="line">
        <TabList mb="1em">
          <Tab>Table</Tab>
          <Tab>Line Graph</Tab>
          <Tab>Bar Graph</Tab>
          <Tab>Pie Chart</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <TableComponent />
          </TabPanel>
          <TabPanel>
            <p>two!</p>
          </TabPanel>
        </TabPanels>
      </Tabs>
      <Drawer
        isOpen={isOpen}
        placement="right"
        onClose={onClose}
        finalFocusRef={btnRef}
        size={"xl"}
      >
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Editing mode</DrawerHeader>

          <DrawerBody>
            <Tabs isFitted variant="enclosed">
              <TabList mb="1em">
                <Tab>Data Manipulation</Tab>
                <Tab>Filtering</Tab>
              </TabList>
              <TabPanels>
                <TabPanel>
                  <p>one!</p>
                </TabPanel>
                <TabPanel>
                  <p>two!</p>
                </TabPanel>
              </TabPanels>
            </Tabs>
          </DrawerBody>

          <DrawerFooter>
            <Button variant="outline" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button onClick={onSave}>Save</Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </Box>
  );
}

export default TableOverview;
