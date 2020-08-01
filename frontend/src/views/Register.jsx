import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import {
  Row,
  Col,
  Form,
  Input,
  Label,
  Alert,
  Button,
  Spinner,
  FormGroup,
} from 'reactstrap';

import { registerBuyer } from '../api/auth';
import GoogleSignInButton from '../components/GoogleSignInButton';

class Register extends Component {

  constructor(props) {
    super(props);
    this.state = {
      name: '',
      email: '',
      message: '',
      password: '',
      cpassword: '',
      loading: false,
      visible: false,
      success: false,
    };
    this.onDismiss = this.onDismiss.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  onDismiss() {
    this.setState({visible: false});
  }

  handleChange(e) {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.setState({loading: true, visible: false});

    // extract data
    const {
      name,
      email,
      password,
      cpassword
    } = this.state;

    if (password !== cpassword) {
      this.setState({
        visible: true,
        loading: false,
        message: 'passwords don\'t match',
      });
      return false;
    }

    registerBuyer(name, email, password).then(data => {
      if (data['error'] !== undefined) {
        const errorMessage = data.error;
        this.setState({
          success: false,
          message: errorMessage,
        });
      } else if (data['token']) {
        this.setState({
          success: true,
          message: 'logged in successfully',
        });
        localStorage.setItem('token', data.token);
      }
    }).catch(err => {
      console.log(err);
    }).finally(() => {
      this.setState({visible: true, loading: false});
    });

  }

  render() {
    return (
      <div>
        <Row>
          <Col sm="12" md={{ size: 4, offset: 4 }}>
            <br />
            <h2 align="center">create account</h2>
            <br />
            <Form onSubmit={this.handleSubmit}>
              <FormGroup>
                <GoogleSignInButton />
                <Col md={12}>
                  <div className="separator">OR</div>
                </Col>
                <Label for="name">name</Label>
                <Input type="text" id="name" onChange={this.handleChange}
                       name="name" autoComplete="off" required autoFocus />
              </FormGroup>
              <FormGroup>
                <Label for="email">email</Label>
                <Input type="email" id="email" onChange={this.handleChange}
                       name="email" autoComplete="off" required />
              </FormGroup>
              <FormGroup>
                <Label for="password">password</Label>
                <Input type="password" id="password" onChange={this.handleChange}
                       name="password" required />
              </FormGroup>
              <FormGroup>
                <Label for="password">confirm password</Label>
                <Input type="password" id="cpassword" onChange={this.handleChange}
                       name="cpassword" required />
              </FormGroup>
              <FormGroup row>
                <Col md={12} className="mb-3">
                  <Button block color="success">
                    create account
                  </Button>
                </Col>
                <Col>
                  <Link to="/authenticate" className="btn btn-primary btn-block">
                    sign in
                  </Link>
                </Col>
                <Col>
                  <Link className="btn btn-danger btn-block mb-3" to="/forgot">
                    forgot password
                  </Link>
                </Col>
              </FormGroup>
              <Col md={12} className="text-center">
                <div className={'mb-3 ' + (this.state.loading ? '' : 'd-none')}>
                  <Spinner color="primary" size="lg" />
                </div>
                <Alert color={this.state.success ? 'success' : 'danger'}
                       isOpen={this.state.visible}
                       toggle={this.onDismiss}>
                  {this.state.message}
                </Alert>
              </Col>
            </Form>
          </Col>
        </Row>
      </div>
    );
  }

}

export default Register;
