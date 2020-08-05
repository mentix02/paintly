import axios from "axios";

const BASE_URL = "/api/buyer/addresses";

const auth_header = (token) => ({
  headers: {
    Authorization: `Token ${token}`,
  },
});

const retData = (res) => res.data;
const retError = (err) => err.response;

axios.defaults.headers.common = { "Content-Type": "multipart/form-data" };

const getAddresses = async () => {
  const token = localStorage.getItem("token");
  try {
    let res = await axios.get(`${BASE_URL}/list/`, auth_header(token));
    return await retData(res);
  } catch (err) {
    return await retError(err);
  }
};

const addAddress = async (address) => {
  const token = localStorage.getItem("token");

  let addressData = new FormData();

  for (let [key, value] of Object.entries(address)) {
    addressData.set(key, String(value));
  }

  try {
    let res = await axios.post(
      `${BASE_URL}/list/`,
      addressData,
      auth_header(token)
    );
    return await retData(res);
  } catch (e) {
    return await retError(e);
  }
};

const deleteAddress = async (addressId) => {
  const url = `${BASE_URL}/delete/${addressId}`,
    token = localStorage.getItem("token");
  try {
    let res = await axios.delete(url, auth_header(token));
    return await retData(res);
  } catch (err) {
    return await retError(err);
  }
};

export { addAddress, getAddresses, deleteAddress };
