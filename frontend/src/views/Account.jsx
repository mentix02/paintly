import React, { useState } from 'react';
import {
  Row,
  Col,
  Nav,
  NavItem,
  TabPane,
  NavLink,
  TabContent,
} from 'reactstrap';
import classnames from 'classnames';

function Account() {

  const [activeTab, setActiveTab] = useState('1');

  const toggle = tab => {
    if (activeTab !== tab) setActiveTab(tab);
  }

  return (
    <div>
      <br/>
      <Row>
        <Col md={{size: 10, offset: 1}} sm={12}>
          <Row>
            <Col md={3} sm={12}>
              <Nav vertical pills>
                <NavItem>
                  <NavLink
                    style={{cursor: 'pointer'}}
                    onClick={() => { toggle('1'); }}
                    className={classnames({ active: activeTab === '1' })}>
                    profile
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink
                    style={{cursor: 'pointer'}}
                    onClick={() => { toggle('2'); }}
                    className={classnames({ active: activeTab === '2' })}>
                    addresses
                  </NavLink>
                </NavItem>
              </Nav>
            </Col>
            <Col md={9} sm={12}>
              <TabContent activeTab={activeTab}>
                <TabPane tabId="1">

                </TabPane>
                <TabPane tabId="2">
                  <h3>addresses</h3>
                </TabPane>
              </TabContent>
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  );
}

export default Account;