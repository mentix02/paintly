import React, {useState, useEffect} from 'react';
import {BsTrashFill, BsDash, BsPlus} from 'react-icons/bs';
import {
  Row,
  Col,
  Card,
  Table,
  Alert,
  Button,
  Spinner,
  CardBody,
  Container,
  CardTitle,
  ButtonGroup,
} from 'reactstrap';

import {
  getCart,
  removeCartItem,
  decrementCartItemQuantity,
  incrementCartItemQuantity,
} from '../api/cart';

function Cart() {

  const [total, setTotal] = useState(0);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const [cartItems, setCartItems] = useState([{
    id: 0, quantity: 0, name: '', price: 0, painting: {name: '', price: 0}
  }]);

  useEffect(() => {
    setLoading(true);
    getCart().then(data => {
      if (data['detail']) {
        setVisible(true);
        setMessage(data.detail);
      } else {
        setTotal(data.reduce(
          (prev, cartItem) =>
            prev + (cartItem.quantity * cartItem.painting.price)
          , 0
        ));
        setCartItems(data);
      }
    }).catch(err => {
      console.log(err);
    }).finally(() => {
      setLoading(false);
    });
  }, [
    setTotal,
    setMessage,
    setLoading,
    setVisible,
    setCartItems,
  ]);

  const sumReduceFunc = (prev, cartItem) => prev + (cartItem.quantity * cartItem.painting.price);

  const handleRemoveButtonClick = function (cart_item_id) {
    removeCartItem(cart_item_id).then(_ => {
      const cartItemsCopy = JSON.parse(JSON.stringify(cartItems));
      const rmIndex = cartItemsCopy.map((item) => item.id).indexOf(cart_item_id);
      cartItemsCopy.splice(rmIndex, 1);
      setCartItems(cartItemsCopy);
      setTotal(cartItemsCopy.reduce(sumReduceFunc, 0));
    }).catch(e => console.log(e));
  };

  const handleDecrementButtonClick = function (cart_item_id) {
    decrementCartItemQuantity(cart_item_id).then(_ => {
      const cartItemsCopy = JSON.parse(JSON.stringify(cartItems));
      const decrementIndex = cartItemsCopy.map((item) => item.id).indexOf(cart_item_id);
      cartItemsCopy[decrementIndex].quantity--;
      if (cartItemsCopy[decrementIndex].quantity === 0)
        cartItemsCopy.splice(decrementIndex, 1);
      setTotal(cartItemsCopy.reduce(sumReduceFunc, 0));
      setCartItems(cartItemsCopy);
    });
  };

  const handleIncrementButtonClick = function (cart_item_id) {
    incrementCartItemQuantity(cart_item_id).then(_ => {
      const cartItemsCopy = JSON.parse(JSON.stringify(cartItems));
      const decrementIndex = cartItemsCopy.map((item) => item.id).indexOf(cart_item_id);
      cartItemsCopy[decrementIndex].quantity++;
      if (cartItemsCopy[decrementIndex].quantity === 0)
        cartItemsCopy.splice(decrementIndex, 1);
      setTotal(cartItemsCopy.reduce(sumReduceFunc, 0));
      setCartItems(cartItemsCopy);
    });
  }

  return (
    <div>
      <Container>
        <br/>
        {
          loading || visible
            ?
            <Row>
              <Col md={{size: 4, offset: 4}} className="text-center">
                <br/>
                <Spinner size="lg" className={loading ? '' : 'd-none'} color="primary"/>
                <Alert color="danger"
                       className={message.length === 0 ? 'd-none' : ''}
                       isOpen={visible}>
                  {message}
                </Alert>
              </Col>
            </Row>
            :
            <Row>
              <Col className={'text-center ' + (loading ? '' : 'd-none')}>
                <br/>
                <br/>
                <Spinner color="primary" size="lg"/>
              </Col>
              <Col className={loading ? 'd-none' : ''} sm={12} md={8}>
                <h3>items</h3>
                <Table responsive borderless>
                  <thead>
                  <tr>
                    <th>name</th>
                    <th>amount</th>
                    <th>price</th>
                    <th>action</th>
                  </tr>
                  </thead>
                  <tbody id="paintings">
                  {
                    cartItems.map((cartItem, index) => (
                      <tr key={index}>
                        <td>{cartItem.painting.name}</td>
                        <td>{cartItem.quantity}</td>
                        <td>₹{cartItem.painting.price * cartItem.quantity}</td>
                        <td>
                          <ButtonGroup>
                            <Button onClick={() => handleDecrementButtonClick(cartItem.id)} size="sm" color="warning">
                              <BsDash style={{color: '#ffffff'}} />
                            </Button>
                            <Button onClick={() => handleRemoveButtonClick(cartItem.id)} size="sm" color="danger">
                              <BsTrashFill/>
                            </Button>
                            <Button onClick={() => handleIncrementButtonClick(cartItem.id)} size="sm" color="success">
                              <BsPlus/>
                            </Button>
                          </ButtonGroup>
                        </td>
                      </tr>
                    ))
                  }
                  </tbody>
                </Table>
              </Col>
              <Col className={loading ? 'd-none' : ''} sm={12} md={4}>
                <Card>
                  <CardBody>
                    <CardTitle>
                      <h4 className="text-center">receipt</h4>
                    </CardTitle>
                    <CardBody>
                      <Table>
                        <thead>
                        <tr>
                          <th>total</th>
                          <th>tax</th>
                          <th>shipping</th>
                        </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>₹{total}</td>
                            <td>15%</td>
                            <td>₹{50}</td>
                          </tr>
                          <tr>
                            <td>{''}</td>
                            <th>final</th>
                            <td>₹ {total + 0.15 * total + 50}</td>
                          </tr>
                        </tbody>
                      </Table>
                    </CardBody>
                  </CardBody>
                </Card>
              </Col>
            </Row>
        }
      </Container>
    </div>
  );
}

export default Cart;
