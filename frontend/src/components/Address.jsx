import React from "react";
import PropTypes from "prop-types";
import { Card, Badge, CardBody, CardText, CardTitle } from "reactstrap";

function Address(props) {
  const { address } = props;

  return (
    <Card outline color={address.primary ? "warning" : ""}>
      <CardBody>
        <CardTitle>
          <h5>
            {address.city}{" "}
            <small>
              {address.primary ? (
                <Badge pill color="warning" className="text-white">
                  primary
                </Badge>
              ) : (
                ""
              )}
            </small>
            <div className="float-right small">#{props.num}</div>
          </h5>
        </CardTitle>
        <CardText>
          {`${address.house_number} ${address.city}, ${address.state} ${address.pin_code}`}
        </CardText>
      </CardBody>
    </Card>
  );
}

Address.propTypes = {
  num: PropTypes.number,
  address: PropTypes.object,
};

export default Address;
