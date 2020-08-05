import React, { useState, useEffect } from "react";
import {
  Row,
  Col,
  Form,
  Input,
  Label,
  Modal,
  Button,
  FormGroup,
  ModalBody,
  ButtonGroup,
  ModalFooter,
  ModalHeader,
} from "reactstrap";
import { FaPen, FaPlus } from "react-icons/fa";

import Address from "./Address";
import { getAddresses, addAddress } from "../api/address";

function Addresses() {
  const [addresses, setAddresses] = useState([]);

  const [isOpen, setIsOpen] = useState(false);
  const toggle = () => setIsOpen(!isOpen);

  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [pinCode, setPinCode] = useState("");
  const [houseNumber, setHouseNumber] = useState("");

  const inputReducers = {
    city: setCity,
    state: setState,
    pinCode: setPinCode,
    houseNumber: setHouseNumber,
  };

  useEffect(() => {
    getAddresses()
      .then((data) => {
        console.log(data);
        setAddresses(data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [setAddresses]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    inputReducers[name](value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const address = {
      city,
      state,
      pin_code: pinCode,
      house_number: houseNumber,
    };
    console.log(address);
    addAddress(address)
      .then((data) => {
        setIsOpen(false);
      })
      .catch((err) => console.log(err));
  };

  return (
    <div>
      <ButtonGroup>
        <Button
          onClick={() => {
            setIsOpen(true);
          }}
          size="sm"
          color="success"
        >
          <FaPlus />
        </Button>
        <Button
          onClick={() => {
            console.log("edit");
          }}
          size="sm"
          color="warning"
        >
          <FaPen style={{ color: "#ffffff" }} />
        </Button>
      </ButtonGroup>
      <br />
      <Row>
        {addresses.map((address, index) => (
          <Col className="mt-2 mb-1" md={6} sm={12} key={index}>
            <Address address={address} num={index + 1} />
          </Col>
        ))}
      </Row>
      <Modal isOpen={isOpen} toggle={toggle}>
        <ModalHeader toggle={toggle}>add address</ModalHeader>
        <ModalBody>
          <Form onSubmit={handleSubmit}>
            <FormGroup>
              <Label for="houseNumber">house number</Label>
              <Input
                required
                id="houseNumber"
                name="houseNumber"
                autoComplete="off"
                onChange={handleChange}
              />
            </FormGroup>
            <FormGroup>
              <Label for="city">city</Label>
              <Input
                id="city"
                name="city"
                autoComplete="off"
                onChange={handleChange}
              />
            </FormGroup>
            <FormGroup>
              <Label for="pinCode">pin code</Label>
              <Input
                id="pinCode"
                name="pinCode"
                autoComplete="off"
                onChange={handleChange}
              />
            </FormGroup>
            <FormGroup>
              <Label for="state">state</Label>
              <Input
                id="state"
                name="state"
                type="select"
                autoComplete="off"
                onChange={handleChange}
              >
                <option value="AP">Andhra Pradesh</option>
                <option value="AR">Arunachal Pradesh</option>
                <option value="AS">Assam</option>
                <option value="BR">Bihar</option>
                <option value="CG">Chhattisgarh</option>
                <option value="GA">Goa</option>
                <option value="GJ">Gujarat</option>
                <option value="HR">Haryana</option>
                <option value="HP">Himachal Pradesh</option>
                <option value="JK">Jammu and Kashmir</option>
                <option value="JH">Jharkhand</option>
                <option value="KA">Karnataka</option>
                <option value="KL">Kerala</option>
                <option value="MP">Madhya Pradesh</option>
                <option value="MH">Maharashtra</option>
                <option value="MN">Manipur</option>
                <option value="ML">Meghalaya</option>
                <option value="MZ">Mizoram</option>
                <option value="NL">Nagaland</option>
                <option value="OR">Orissa</option>
                <option value="PB">Punjab</option>
                <option value="RJ">Rajasthan</option>
                <option value="SK">Sikkim</option>
                <option value="TN">Tamil Nadu</option>
                <option value="TR">Tripura</option>
                <option value="UK">Uttarakhand</option>
                <option value="UP">Uttar Pradesh</option>
                <option value="WB">West Bengal</option>
                <option value="AN">Andaman and Nicobar Islands</option>
                <option value="CH">Chandigarh</option>
                <option value="DH">Dadra and Nagar Haveli</option>
                <option value="DD">Daman and Diu</option>
                <option value="DL">Delhi</option>
                <option value="LD">Lakshadweep</option>
                <option value="PY">Pondicherry</option>
              </Input>
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button size="sm" color="danger" onClick={toggle}>
            cancel
          </Button>{" "}
          <Button size="sm" color="success" onClick={handleSubmit}>
            add
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  );
}

export default Addresses;
