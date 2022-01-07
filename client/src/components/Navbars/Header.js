import React from "react";
import { ReactComponent as Logo } from "./Logo.svg";
import { Box, Divider } from "@chakra-ui/react";
function Header() {
  return (
    <Box mb="2%">
      <Logo style={{ width: "14%", height: "7%" }} />
    </Box>
  );
}

export default Header;
