import React, {useState, useEffect, useCallback} from 'react';
import {BsLightningFill} from 'react-icons/bs';
// noinspection ES6CheckImport
import {useHistory, useLocation} from 'react-router-dom';
import {
  FaAngleUp,
  FaCartPlus,
  FaAngleDown,
} from 'react-icons/fa';
import {
  Card,
  Button,
  CardImg,
  CardBody,
  Collapse,
  CardTitle,
  ButtonGroup,
  CardSubtitle,
} from 'reactstrap';

import store from '../store';
import {addToCart} from '../api/cart';
import DisabledLink from '../components/DisabledLink';

function Painting(props) {

  const {painting} = props;

  const history = useHistory();
  const location = useLocation();
  const [tags, setTags] = useState([]);
  const [collapsed, setCollapsed] = useState(true);

  const getTagsFromSearch = useCallback(url => {
    const query = url.substr(1);
    const tempTags = query.substr(query.indexOf('=') + 1).split(',');
    if (tempTags.length === 1 && tempTags[0].length === 0)
      return [];
    else
      return tempTags;
  }, [])
  
  useEffect(() => {
    setTags(getTagsFromSearch(location.search));
  }, [setTags, location, getTagsFromSearch])

  const toggle = () => setCollapsed(!collapsed);
  const handleCartClick = () => {

    // Check if logged in.
    if (!store.isLoggedIn) {
      history.push('/authenticate')
    }

    const painting_id = painting.id;
    addToCart(painting_id).then(_ => {
      history.push('/cart');
    }).catch(err => {
      console.log(err);
    });
  };

  function appendBadgeLink(tag) {
    const prevTags = getTagsFromSearch(location.search);
    if (tags.length === 0)
      return `${location.pathname}?tags=${tag}`;
    else
      return `${location.pathname}?tags=${prevTags.join(',')},${tag}`;
  }

  const toCurrency = num => num.toLocaleString().split(/\s/).join(',');

  return (
    <Card>
      <CardImg top height="375px" alt={painting.name} src={painting.thumbnail}/>
      <CardBody>
        <CardTitle><h5>{painting.name}</h5></CardTitle>
        <CardSubtitle>
          <h6 className="mt-4">
            {painting.height}x{painting.width} inches at ₹{toCurrency(painting.price)}
          </h6>
          <ButtonGroup>
            {
              painting.tags.map((tag, index) => (
                <DisabledLink disabled={tags.includes(tag)} to={appendBadgeLink(tag)}
                      className="badge badge-secondary badge-pill" key={index}>
                  {tag}
                </DisabledLink>
              ))
            }
          </ButtonGroup>
        </CardSubtitle>
        <hr/>
        <div>
          <ButtonGroup className="float-right">
            <Button onClick={handleCartClick} color="success">
              <FaCartPlus/>
            </Button>
            <Button color="warning">
              <BsLightningFill style={{color: "#ffffff"}}/>
            </Button>
            <Button onClick={toggle} color="primary">
              {
                collapsed ? <FaAngleDown/> : <FaAngleUp/>
              }
            </Button>
          </ButtonGroup>
          <Collapse isOpen={!collapsed}>
            <br/><br/>
            {painting.description}
          </Collapse>
        </div>
      </CardBody>
    </Card>
  );
}

export default Painting;
