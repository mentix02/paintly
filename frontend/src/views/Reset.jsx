import React, { useState, useEffect } from "react";
import { useParams, useHistory } from "react-router-dom";
import {
  Row,
  Col,
  Form,
  Input,
  Alert,
  Button,
  Spinner,
  FormGroup,
} from "reactstrap";

import { validateResetToken, resetPassword } from "../api/auth";

function Reset() {
  const history = useHistory();
  const { token } = useParams();
  const [message, setMessage] = useState("");
  const [password, setPassword] = useState("");
  const [success, setSuccess] = useState(false);
  const [visible, setVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [tokValid, settokValid] = useState(false);
  const [cpassword, setCPassword] = useState("");
  const inputReducers = {
    password: setPassword,
    cpassword: setCPassword,
  };

  const displayError = (msg) => {
    setVisible(true);
    setLoading(false);
    setSuccess(false);
    setMessage(msg);
  };

  useEffect(() => {
    validateResetToken(token)
      .then((data) => {
        if (data["error"]) {
          displayError(data.message);
        } else {
          settokValid(true);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [token]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    if (password !== cpassword) {
      displayError("Passwords don't match.");
      return false;
    } else if (password.length < 8) {
      displayError("Password has to be more than 8 characters.");
      return false;
    }

    resetPassword(token, password)
      .then((data) => {
        if (data["error"]) {
          displayError(data.message);
        } else {
          setVisible(true);
          setLoading(false);
          setSuccess(true);
          setMessage(data.message);
          setTimeout(() => history.push("/authenticate"), 3000);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    inputReducers[name](value);
  };

  const onDismiss = () => {
    setVisible(false);
  };

  return (
    <div>
      <Row>
        <Col sm="12" md={{ size: 4, offset: 4 }}>
          <br />
          <h2 align="center">new password</h2>
          <br />
          <Form onSubmit={handleSubmit}>
            <FormGroup className={tokValid ? "" : "d-none"} row>
              <Col md={12} className="mb-3">
                <Input
                  type="password"
                  id="password"
                  onChange={handleChange}
                  name="password"
                  placeholder="new password"
                  autoComplete="off"
                  required
                />
              </Col>
              <Col md={12} className="mb-3">
                <Input
                  type="password"
                  id="cpassword"
                  onChange={handleChange}
                  name="cpassword"
                  placeholder="confirm password"
                  autoComplete="off"
                  required
                />
              </Col>
              <Col>
                <Button block color="success">
                  set password
                </Button>
              </Col>
            </FormGroup>
            <FormGroup row>
              <Col md={12} className="text-center">
                <div className={"mb-3 " + (loading ? "" : "d-none")}>
                  <Spinner color="primary" size="lg" />
                </div>
                <Alert
                  color={success ? "success" : "danger"}
                  toggle={tokValid ? onDismiss : null}
                  isOpen={visible}
                >
                  {message}
                </Alert>
              </Col>
            </FormGroup>
          </Form>
        </Col>
      </Row>
    </div>
  );
}

export default Reset;
