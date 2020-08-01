import React, { useState } from 'react';
import { Route, Redirect } from 'react-router-dom';

function PrivateRoute({ children, ...rest }) {

  const isLoggedIn = useState(
    localStorage.getItem('token') !== null
  );

  return (
    <Route
      {...rest}
      render={({ _ }) =>
        isLoggedIn[0] ? (
          children
        ) : (
          <Redirect
            to='/authenticate'
          />
        )
      }
    />
  );
}

export default PrivateRoute;
