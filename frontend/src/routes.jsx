import React from "react";
import { Route, Switch } from "react-router-dom";

import Home from "./views/Home";
import Cart from "./views/Cart";
import Reset from "./views/Reset";
import Forgot from "./views/Forgot";
import Contact from "./views/Contact";
import Account from "./views/Account";
import Register from "./views/Register";
import Authenticate from "./views/Authenticate";
import PrivateRoute from "./components/PrivateRoute";

const BaseRouter = () => (
  <Switch>
    <Route exact path="/" component={Home} />
    <Route path="/forgot" component={Forgot} />
    <Route path="/contact" component={Contact} />
    <Route path="/register" component={Register} />
    <Route path="/reset/:token" component={Reset} />
    <Route path="/reset/:token" component={Reset} />
    <Route path="/authenticate" component={Authenticate} />
    <PrivateRoute path="/cart">
      <Route path="/cart" component={Cart} />
    </PrivateRoute>
    <PrivateRoute path="/account">
      <Route path="/account" component={Account} />
    </PrivateRoute>
  </Switch>
);

export default BaseRouter;
