import {
  extendTheme,
  withDefaultColorScheme,
  theme as baseTheme,
} from "@chakra-ui/react";
import { Input } from "./components/input.theme";
import { mode } from "@chakra-ui/theme-tools";
import { Button } from "./components/button.theme";
export const customTheme = extendTheme(
  {
    colors: {
      primary: baseTheme.colors.teal,
      border: "teal.300",
      dark: {
        100: "#2E3440",
        200: "#292E39",
      },
      light: {
        100: "#FFFFFF",
        200: "#F8F9FB",
      },
    },
    styles: {
      global: (props) => ({
        body: {
          bg: mode("#f8f9fb", "#292E39")(props),
        },
      }),
    },
    components: {
      Input,
      Button,
    },
  },
  withDefaultColorScheme({ colorScheme: "primary" })
);
