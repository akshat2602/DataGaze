import React, { useState } from "react";
import {
  Box,
  Button,
  Text,
  Input,
  InputGroup,
  InputLeftElement,
  FormControl,
  Center,
  Image,
  useColorModeValue
} from "@chakra-ui/react";
import { BsFillPersonFill } from "react-icons/bs";
import { FiKey } from "react-icons/fi";
function Login() {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const bg = useColorModeValue("light.100", "dark.100");
  const onSubmit = () => {
    //TODO: Integrate with Redux
    const data = {
      username: credentials.username,
      password: credentials.password,
    };
    console.log(credentials);
    // axios
    //   .post(`${process.env.REACT_APP_BACKEND_URL}/auth/login/`, data)
    //   .then((res) => {
    //     // console.log(res);
    //     const data = {
    //       access_token: res.data.access_token,
    //       refresh_token: res.data.refresh_token,
    //       type: "LOGIN_SUCCESSFUL",
    //     };
    //     console.log(data);
    //     // dispatch(authActions(data));
    //     // history.push("/volunteer-dashboard");
    //   })
    //   .catch((err) => {
    //     console.log(err);
    //     // const data = {
    //     //   type: "AUTHENTICATION_ERROR"
    //     // }
    //     // dispatch()
    //   });
  };
  return (
    <Box w="100%" h="100vh" verticalAlign="center">
      <Center h="100%">
        <Box w="40%" bg={bg} p="3%" borderRadius="xl">
          <Center>
            <Image src="Logo.svg" />
          </Center>
          <Text fontWeight="bold" mb="1" fontSize="4xl">
            Login
          </Text>
          <Text fontWeight="light" color="gray" mb="5" fontSize="xl">
            Please enter your credentials
          </Text>
          <FormControl id="username" isRequired>
            <InputGroup mb="3">
              <InputLeftElement color="teal" children={<BsFillPersonFill />} />
              <Input
                name="username"
                value={credentials.username}
                onChange={(e) =>
                  setCredentials({
                    ...credentials,
                    username: e.target.value,
                  })
                }
                placeholder="Username"
              />
            </InputGroup>
          </FormControl>
          <FormControl id="password" isRequired>
            <InputGroup>
              <InputLeftElement color="teal" children={<FiKey />} />
              <Input
                name="password"
                value={credentials.password}
                onChange={(e) =>
                  setCredentials({
                    ...credentials,
                    password: e.target.value,
                  })
                }
                type="password"
                placeholder="Password"
              />
            </InputGroup>
          </FormControl>
          <Button mt="2%" type="submit" variant="solid" onClick={onSubmit}>
            Login
          </Button>
        </Box>
      </Center>
    </Box>
  );
}

export default Login;
