import React from "react";
import { ReactComponent as Logo } from "./Logo.svg";
import { ReactComponent as LogoWhite } from "./Logo_white.svg";
import { Box, color, Divider } from "@chakra-ui/react";
import { useColorMode } from "@chakra-ui/react";

function Header() {
  const { toggleColorMode, colorMode } = useColorMode();
  return (
    <Box mb="2%">
      {colorMode === "light" ? (
        <LogoWhite style={{ width: "14%", height: "7%" }} />
      ) : (
        <Logo style={{ width: "14%", height: "7%" }} />
      )}
    </Box>
  );
}

export default Header;
