import React, { useState } from "react";
import {
  FormControl,
  Select,
  Button,
  InputLabel,
  MenuItem,
  TextField,
} from "@mui/material";
import { deviceTypes } from "../constants/device";

import "./home.css";

const Home = () => {
  const [deviceType, setDeviceType] = useState("");
  const [deviceId, setDeviceId] = useState("");
  const [key, setKey] = useState("");

  const handleDeviceTypeChange = (event) => {
    setDeviceType(event.target.value);
  };

  const handleDeviceIdChange = (event) => {
    setDeviceId(event.target.value);
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
      <Button variant="outlined" color="success">
        Verify User
      </Button>
    </div>
  );
};

export default Home;
