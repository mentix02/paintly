import React from 'react';
import {
  Row,
  Col,
  Form,
  Label,
  Input,
  FormGroup,
} from 'reactstrap';

function AccountEditForm() {
  return (
    <Row>
      <Col sm="12" md={{ size: 4, offset: 4 }}>
        <Form>
          <FormGroup>
            <Label for="name">name</Label>
            <Input id="name" />
          </FormGroup>
        </Form>
      </Col>
    </Row>
  );
}

export default AccountEditForm;
