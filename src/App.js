import React from "react"
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./screens/home";

function App() {
  return (
    <BrowserRouter>
        <div className="root">
            <Routes>
              <Route path="/" element={<Home />} />
            </Routes>
        </div>
    </BrowserRouter>
  );
}

export default App;
