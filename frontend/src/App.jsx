import React from "react";
import { BrowserRouter as Router } from "react-router-dom";

import BaseRouter from "./routes";
import Navigation from "./components/Navigation";

import { Container } from "reactstrap";

function App() {
  return (
    <div>
      <Router>
        <div>
          <Navigation />
          <Container>
            <BaseRouter />
          </Container>
        </div>
      </Router>
    </div>
  );
}

export default App;
