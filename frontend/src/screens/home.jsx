import React, { useState } from "react";
import { Button, TextField, Box } from "@mui/material";
import axios from "axios";

import "./home.css";

const Home = () => {
  const [deviceId, setDeviceId] = useState("");
  const [key, setKey] = useState("");
  const [message, setMessage] = useState("");

  const handleDeviceIdChange = (event) => {
    setDeviceId(event.target.value);
  };

  const registerDevice = () => {
    setMessage("Registering...");

    axios({
      method: "post",
      url: `http://localhost:8000/controller/`,
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        privKey: key,
        deviceId: deviceId,
      },
    })
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((err) => {
        console.log(err);
        setMessage(err.code + ": Error occured while registering");
      });
  };

  const authenticateUser = () => {
    setMessage("Authenticating...");

    axios({
      method: "post",
      url: `http://localhost:8000/controller/auth/`,
      headers: {
        "Content-Type": "application/json",
      },
      data: {
        privKey: key,
        deviceId: deviceId,
      },
    })
      .then((response) => {
        let message = "Successfully authenticated"
        if (response.data.message === "False") {
          message = "Authentication failed"
        }
        setMessage(message);
      })
      .catch((err) => {
        console.log(err);
        setMessage(err.code + ": Error occured while authenticating you");
      });
  };

  const handleKeyChange = (event) => {
    setKey(event.target.value);
  };

  return (
    <div className="container">
      <TextField
        label="Device ID"
        variant="outlined"
        value={deviceId}
        onChange={handleDeviceIdChange}
        fullWidth
      />

      <TextField
        label="Private Key"
        variant="outlined"
        value={key}
        onChange={handleKeyChange}
        fullWidth
      />

      <br />
      <Button variant="outlined" color="success" onClick={registerDevice}>
        Register Device
      </Button>

      <Button variant="outlined" color="success" onClick={authenticateUser}>
        Authenticate User
      </Button>

      <Box fullWidth className="message-container">
        {message}
      </Box>
    </div>
  );
};

export default Home;
