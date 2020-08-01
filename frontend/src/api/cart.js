import axios from 'axios';

const BASE_URL = '/api/cart';

const auth_header = (token) => ({
  headers: {
    Authorization: `Token ${token}`
  }
});

const retData = res => res.data;
const retError = err => err.response;

axios.defaults.headers.common = {'Content-Type': 'multipart/form-data'};

const getCart = async () => {
  const token = localStorage.getItem('token');
  try {
    let res = await axios.get(`${BASE_URL}/items/`, auth_header(token));
    return await retData(res);
  } catch (err) {
    return await retError(err);
  }
};

const addToCart = async painting_id => {
  const token = localStorage.getItem('token');
  let paintingIdData = new FormData();
  paintingIdData.set('painting_id', painting_id);
  try {
    let res = await axios.post(`${BASE_URL}/add/`, paintingIdData, auth_header(token));
    return await retData(res);
  } catch (err) {
    return await retError(err);
  }
};

const removeCartItem = async cart_item_id => {
  const token = localStorage.getItem('token');
  let cartItemData = new FormData();
  cartItemData.set('cart_item_id', cart_item_id);
  try {
    let res = await axios.post(`${BASE_URL}/remove/`, cartItemData, auth_header(token));
    return await retData(res);
  } catch (err) {
    return await retError(err);
  }
};

const mutateCartItemQuantity = async (cart_item_id, increment) => {
  const token = localStorage.getItem('token');
  let cartItemData = new FormData();
  cartItemData.set('cart_item_id', cart_item_id);
  try {
    let res = await axios.post(`${BASE_URL}/${
      increment ? 'increment' : 'decrement'
    }/`, cartItemData, auth_header(token));
    return await retData(res);
  } catch (err) {
    return await retError(err);
  }
};

const incrementCartItemQuantity = cart_item_id => {
  return mutateCartItemQuantity(cart_item_id, true);
};

const decrementCartItemQuantity = cart_item_id => {
  return mutateCartItemQuantity(cart_item_id, false);
};

export {
  getCart,
  addToCart,
  removeCartItem,
  incrementCartItemQuantity,
  decrementCartItemQuantity,
};
