import React, {useState} from "react";
import {
  Row,
  Col,
  Form,
  Input,
  FormGroup, Button, Spinner, Alert,
} from 'reactstrap';

function Contact() {

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [visible, setVisible] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const inputReducers = {
    name: setName,
    email: setEmail,
    content: setContent,
  };

  const onDismiss = () => {
    setVisible(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    inputReducers[name](value);
  };

  const handleSubmit = e => {
    e.preventDefault();
    console.log('name', name);
    console.log('email', email);
    console.log('content', content);
    setSubmitted(true);
  };

  return (
    <Row>
      <Col md={{size: 4, offset: 4}}>
        <br/>
        <h3 className="text-center">contact us</h3>
        <br />
        <Form onSubmit={handleSubmit}>
          <FormGroup className={submitted ? 'd-none' : ''} row>
            <Col md={12} className="mb-3">
              <Input type="text" id="name" onChange={handleChange}
                     name="name" placeholder="name" autoComplete="off" autoFocus required />
            </Col>
            <Col md={12} className="mb-3">
              <Input type="email" id="email" onChange={handleChange}
                     name="email" placeholder="email" autoComplete="off" required />
            </Col>
            <Col md={12} className="mb-3">
              <Input type="textarea" id="content" onChange={handleChange}
                     name="content" placeholder="body" rows={5} autoComplete="off" required />
            </Col>
            <Col className="mb-3">
              <Button block color="primary">
                message us
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
  );
}

export default Contact;
