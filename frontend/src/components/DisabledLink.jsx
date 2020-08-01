import React from 'react';
import {Link} from 'react-router-dom';

function DisabledLink({ children, to, disabled, ...rest }) {
  return disabled ? <span {...rest}>{children}</span> : <Link {...rest} to={to}>{children}</Link>;
}

export default DisabledLink;
