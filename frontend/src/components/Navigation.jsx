import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FaUser } from "react-icons/fa";
// noinspection ES6CheckImport
import { useHistory, useLocation } from "react-router-dom";
import {
  Nav,
  Navbar,
  NavItem,
  Collapse,
  Container,
  DropdownMenu,
  DropdownItem,
  NavbarToggler,
  DropdownToggle,
  UncontrolledDropdown,
} from "reactstrap";

import store from "../store";

function Navigation() {
  const history = useHistory();
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const [dropdownIsOpen, setDropdownIsOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);
  const close = () => {
    if (isOpen) setIsOpen(false);
  };

  const toggleDropdown = () => setDropdownIsOpen(!dropdownIsOpen);
  const closeDropdown = () => {
    if (dropdownIsOpen) setDropdownIsOpen(false);
  };

  const signOut = () => {
    localStorage.removeItem("token");
    history.push("/");
    window.location.reload();
  };

  return (
    <Navbar color="light" light expand="md">
      <Container>
        <Link onClick={close} className="navbar-brand" to="/">
          paintly
        </Link>
        <NavbarToggler onClick={toggle} />
        <Collapse isOpen={isOpen} navbar>
          <Nav onClick={close} className="mr-auto" navbar>
            <NavItem active={location.pathname === "/"}>
              <Link className="nav-link" to="/">
                paintings
              </Link>
            </NavItem>
            <NavItem active={location.pathname === "/about"}>
              <Link className="nav-link" to="/about">
                about
              </Link>
            </NavItem>
            <NavItem active={location.pathname === "/contact"}>
              <Link className="nav-link" to="/contact">
                contact
              </Link>
            </NavItem>
          </Nav>
          <Nav onClick={close} className="mr-4" navbar>
            {store.isLoggedIn ? (
              <>
                <NavItem active={location.pathname === "/cart"}>
                  <Link to="/cart" className="nav-link">
                    cart
                  </Link>
                </NavItem>
                <UncontrolledDropdown
                  nav
                  inNavbar
                  isOpen={dropdownIsOpen}
                  active={location.pathname === "/account"}
                >
                  <DropdownToggle onClick={toggleDropdown} nav caret>
                    <FaUser />
                  </DropdownToggle>
                  <DropdownMenu onClick={closeDropdown} right>
                    <Link className="dropdown-item" to="/account">
                      account
                    </Link>
                    <DropdownItem divider />
                    <DropdownItem onClick={() => signOut()}>
                      sign out
                    </DropdownItem>
                  </DropdownMenu>
                </UncontrolledDropdown>
              </>
            ) : (
              <>
                <NavItem>
                  <Link to="/register" className="nav-link">
                    register
                  </Link>
                </NavItem>
                <NavItem>
                  <Link to="/authenticate" className="nav-link">
                    sign in
                  </Link>
                </NavItem>
              </>
            )}
          </Nav>
        </Collapse>
      </Container>
    </Navbar>
  );
}

export default Navigation;
