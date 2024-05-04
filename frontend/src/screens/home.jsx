import React, { useState } from "react";
import {
  FormControl,
  Select,
  Button,
  InputLabel,
  MenuItem,
  TextField,
  Box,
} from "@mui/material";
import { deviceTypes } from "../constants/device";
import axios from "axios";

import "./home.css";

const Home = () => {
  const [deviceType, setDeviceType] = useState("");
  const [deviceId, setDeviceId] = useState("");
  const [key, setKey] = useState("");
  const [message, setMessage] = useState("");

  const handleDeviceTypeChange = (event) => {
    setDeviceType(event.target.value);
  };

  const handleDeviceIdChange = (event) => {
    setDeviceId(event.target.value);
  };

  const getMessage = () => {
    setMessage("Authenticating...");

    axios({
      method: "get",
      url: `http://localhost:8000/controller/`,
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        setMessage("Here's the message hash: " + response.data.message);
      })
      .catch((err) => {
        console.log(err);
        setMessage(err.code + ": Error occured while authenticating you");
      });
  };

  const getAuth1 = () => {
    setMessage("Authenticating...");

    axios({
      method: "get",
      url: `http://localhost:8000/controller/auth1/`,
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        setMessage("Here's the message hash: " + response.data.message);
      })
      .catch((err) => {
        console.log(err);
        setMessage(err.code + ": Error occured while authenticating you");
      });
  };

  const getAuth2 = () => {
    setMessage("Authenticating...");

    axios({
      method: "get",
      url: `http://localhost:8000/controller/auth2/`,
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        setMessage("Here's the message hash: " + response.data.message);
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
      <FormControl fullWidth>
        <InputLabel>Device Type</InputLabel>
        <Select
          value={deviceType}
          label="Device Type"
          onChange={handleDeviceTypeChange}
        >
          {deviceTypes.map(({ deviceTypeSlug, deviceTypeName }, _) => {
            return <MenuItem value={deviceTypeSlug}>{deviceTypeName}</MenuItem>;
          })}
        </Select>
      </FormControl>

      <TextField
        label="Device ID"
        variant="outlined"
        value={deviceId}
        onChange={handleDeviceIdChange}
        fullWidth
      />

      <TextField
        label="Key"
        variant="outlined"
        value={key}
        onChange={handleKeyChange}
        fullWidth
      />

      <br />
      <Button variant="outlined" color="success" onClick={getMessage}>
        Register Device
      </Button>

      <Button variant="outlined" color="success" onClick={getAuth1}>
        Verify User Auth1
      </Button>

      <Button variant="outlined" color="success" onClick={getAuth2}>
        Verify User Auth2
      </Button>
      <Box fullWidth className="message-container">
        {message}
      </Box>
    </div>
  );
};

export default Home;
