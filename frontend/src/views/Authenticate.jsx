import "./css/Authenticate.css";

import { Link } from "react-router-dom";
import React, { Component } from "react";
import {
  Row,
  Col,
  Form,
  Alert,
  Input,
  Button,
  Spinner,
  FormGroup,
} from "reactstrap";

import { getAuthToken } from "../api/auth";
import GoogleSignInButton from "../components/GoogleSignInButton";

class Authenticate extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      message: "",
      password: "",
      loading: false,
      visible: false,
      success: false,
    };
    this.onDismiss = this.onDismiss.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  onDismiss() {
    this.setState({ visible: false });
  }

  handleChange(e) {
    const target = e.target;
    const name = target.name;
    this.setState({ [name]: target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.setState({ loading: true, visible: false });

    // extract email and password
    const { email, password } = this.state;

    // make api call
    getAuthToken(email, password)
      .then((data) => {
        if (data["non_field_errors"] !== undefined) {
          const errorMessage = data["non_field_errors"][0];
          this.setState({
            success: false,
            message: errorMessage,
          });
        } else if (data["token"]) {
          this.setState({
            success: true,
            message: "logged in successfully",
          });
          localStorage.setItem("token", data.token);
        }
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {
        this.setState({ visible: true, loading: false });
      });
  }

  render() {
    return (
      <div>
        <Row>
          <Col sm="12" md={{ size: 4, offset: 4 }}>
            <br />
            <h2 align="center">account login</h2>
            <br />
            <Form onSubmit={this.handleSubmit}>
              <FormGroup row>
                <Col sm={12} md={12}>
                  <GoogleSignInButton />
                </Col>
                <Col>
                  <div className="separator">OR</div>
                </Col>
                <Col sm={6} md={12} className="mb-3">
                  <Input
                    type="email"
                    id="email"
                    onChange={this.handleChange}
                    name="email"
                    placeholder="email"
                    autoComplete="off"
                    required
                  />
                </Col>
                <Col sm={6} md={12} className="mb-3">
                  <Input
                    type="password"
                    id="password"
                    onChange={this.handleChange}
                    name="password"
                    placeholder="password"
                    required
                  />
                </Col>
                <Col md={12} className="mb-3">
                  <Button block color="success">
                    sign in
                  </Button>
                </Col>
                <Col>
                  <Link to="/register" className="btn btn-primary btn-block">
                    create account
                  </Link>
                </Col>
                <Col>
                  <Link className="btn btn-danger btn-block mb-3" to="/forgot">
                    forgot password
                  </Link>
                </Col>
                <Col md={12} className="text-center">
                  <div
                    className={"mb-3 " + (this.state.loading ? "" : "d-none")}
                  >
                    <Spinner color="primary" size="lg" />
                  </div>
                  <Alert
                    color={this.state.success ? "success" : "danger"}
                    isOpen={this.state.visible}
                    toggle={this.onDismiss}
                  >
                    {this.state.message}
                  </Alert>
                </Col>
              </FormGroup>
            </Form>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Authenticate;
