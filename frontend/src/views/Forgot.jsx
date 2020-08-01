import React, { useState } from 'react';
import { 
  Row, 
  Col,
  Form,
  Alert,
  Input,
  Button,
  Spinner,
  FormGroup
} from 'reactstrap';

import { sendResetPasswordLink } from '../api/auth';

function Forgot() {

  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [success, setSuccess] = useState(false);
  const [visible, setVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const inputReducers = {
    email: setEmail,
  };

  const handleSubmit = e => {
    e.preventDefault();

    setLoading(true);
    setVisible(false);
    console.log(email);

    // make api call
    sendResetPasswordLink(email).then(data => {
      if (data['error']) {
        setSuccess(false);
        setMessage(data.error);
      } else {
        setSuccess(true);
        setMessage(data.message);
      }
    }).catch(err => {
      console.log(err);
    }).finally(() => {
      setVisible(true);
      setLoading(false);
      setSubmitted(true);
    });

  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    inputReducers[name](value);
  };

  return (
    <div>
      <Row>
        <Col sm="12" md={{ size: 4, offset: 4 }}>
          <br />
          <h2 className="text-center">reset password</h2>
          <br />
          <Form onSubmit={handleSubmit}>
            <FormGroup className={submitted ? 'd-none' : ''} row>
              <Col md={12} className="mb-3">
                <Input type="email" id="email" onChange={handleChange}
                       name="email" placeholder="email" autoComplete="off" required />
              </Col>
              <Col className="mb-3">
                <Button block color="primary">
                  send reset link
                </Button>
              </Col>
            </FormGroup>
            <FormGroup row>
              <Col md={12} className="text-center">
                <div className={'mb-3 ' + (loading ? '' : 'd-none')}>
                  <Spinner color="primary" size="lg" />
                </div>
                <Alert color={success ? 'success' : 'danger'}
                       isOpen={visible}>
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

export default Forgot;
